"""
FluView / FluSurv-NET replication of the Paper 3 specification curve.

Runs the design in claude/fluview_replication_plan.md, section 4, and scores
P14-P18 from section 5. Deviations are printed at the head of the output.

Read-only on inputs. Reads us/raw.json, the pinned Delphi Epidata pull, so the
replication rebuilds without network access. Writes us/fluview_speccurve.csv,
us/baselines.csv and us/fluview_estimates.csv.
"""
import itertools
import json
import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as st

# Paths resolve from the repository root, so the script runs from anywhere.
ROOT = Path(__file__).resolve().parents[1]
US = ROOT / "us"
RAW = US / "raw.json"

CHANNELS = {
    "rate_age_0tlt1": "Hospitalisation <1y", "rate_age_1t4": "Hospitalisation 1-4y",
    "rate_age_5t11": "Hospitalisation 5-11y", "rate_age_12t17": "Hospitalisation 12-17y",
    "rate_age_18t29": "Hospitalisation 18-29y", "rate_age_30t39": "Hospitalisation 30-39y",
    "rate_age_40t49": "Hospitalisation 40-49y", "rate_age_gte75": "Hospitalisation 75+y",
    "rate_overall": "Hospitalisation all ages", "wili": "ILINet weighted ILI",
}

STAT = ["sd1.645", "sd1.96", "sd2.0", "sd2.58", "p90", "p95", "p97.5"]
NONSEASON = [0.25, 0.40, 0.50]
COVID = ["exclude_2020_2022", "exclude_2020", "include_all"]
SMOOTH = [False, True]
SUSTAIN = [1, 2]
REFPERIOD = ["rolling3", "all_history"]
COMPARATOR = ["ilinet_published", "positivity_derived", "ili_derived"]
ANCHOR = ["reference_series", "own_series"]


def ew_to_date(ew):
    """MMWR week -> Thursday of that week (midpoint), matching the HK MidDate convention."""
    y, w = int(str(ew)[:4]), int(str(ew)[4:])
    jan1 = dt.date(y, 1, 1)
    # MMWR week 1 contains Jan 4 / first Wednesday; anchor on the Sunday start
    start = jan1 - dt.timedelta(days=(jan1.weekday() + 1) % 7)
    if dt.date(y, 1, 1).weekday() in (3, 4, 5):      # Thu/Fri/Sat -> week 1 starts next Sunday
        start += dt.timedelta(days=7)
    return pd.Timestamp(start + dt.timedelta(days=7 * (w - 1) + 3))


def season_of(d):
    """US season label: week 40 of year Y to week 20 of Y+1."""
    y = d.year
    return f"{y}/{str(y+1)[2:]}" if d.month >= 8 else f"{y-1}/{str(y)[2:]}"


def load():
    r = json.load(open(RAW))
    cl = pd.DataFrame(r["fluview_clinical"])[
        ["epiweek", "percent_positive", "total_a", "total_b", "total_specimens", "issue"]]
    il = pd.DataFrame(r["fluview"])[["epiweek", "wili", "issue"]]
    fs = pd.DataFrame(r["flusurv"])
    keep = ["epiweek", "issue"] + [c for c in CHANNELS if c.startswith("rate")]
    fs = fs[[c for c in keep if c in fs.columns]]

    d = fs.merge(cl.drop(columns="issue"), on="epiweek", how="inner") \
          .merge(il.drop(columns="issue"), on="epiweek", how="left")
    d["MidDate"] = d.epiweek.map(ew_to_date)
    d["season"] = d.MidDate.map(season_of)
    d = d.sort_values("epiweek").reset_index(drop=True)
    d["pos_total"] = d.total_a.fillna(0) + d.total_b.fillna(0)
    return d, int(fs.issue.max()), int(cl.issue.max())


def cdc_noninfluenza_weeks(d, season):
    """CDC: >=2 consecutive weeks each <2% of the season's total positives."""
    s = d[d.season == season]
    if s.empty or s.pos_total.sum() == 0:
        return pd.Index([])
    frac = s.pos_total / s.pos_total.sum()
    low = (frac < 0.02).values
    keep = np.zeros(len(s), bool)
    i = 0
    while i < len(low):
        if low[i]:
            j = i
            while j < len(low) and low[j]:
                j += 1
            if j - i >= 2:
                keep[i:j] = True
            i = j
        else:
            i += 1
    return s.index[keep]


def cdc_baseline(d, season, seasons_order):
    """Mean wILI in non-influenza weeks of the 3 most recent prior seasons + 2 SD."""
    k = seasons_order.index(season)
    prior = seasons_order[max(0, k - 3):k]
    idx = pd.Index([])
    for p in prior:
        idx = idx.union(cdc_noninfluenza_weeks(d, p))
    v = d.loc[idx, "wili"].dropna()
    return float(v.mean() + 2 * v.std()) if len(v) >= 5 else np.nan


def threshold(values, stat):
    v = pd.Series(values).dropna()
    if len(v) < 5:
        return np.inf
    if stat.startswith("sd"):
        return v.mean() + float(stat[2:]) * v.std()
    return v.quantile(float(stat[1:]) / 100.0)


def first_crossing(series, dates, thr, sustain):
    a = (np.asarray(series, float) > thr)
    for i in range(len(a) - sustain + 1):
        if a[i:i + sustain].all():
            return dates.iloc[i]
    return None


def covid_mask(d, mode):
    if mode == "exclude_2020_2022":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2022-12-31"))
    if mode == "exclude_2020":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2020-12-31"))
    return pd.Series(True, index=d.index)


def main():
    d0, iss_fs, iss_cl = load()
    SEASONS = sorted(d0.season.unique())
    print(f"weeks {len(d0)}  seasons {len(SEASONS)}: {SEASONS}")
    print(f"issue pinned: flusurv {iss_fs}, fluview_clinical {iss_cl}; retrieved 2026-09-04")

    # ---- reconstructed CDC baselines, validated against the two published values
    base = {s: cdc_baseline(d0, s, SEASONS) for s in SEASONS}
    print("\n=== RECONSTRUCTED ILINet NATIONAL BASELINES (CDC method) ===")
    known = {"2024/25": 3.0, "2025/26": 3.1}
    rows = []
    for s in SEASONS:
        k = known.get(s)
        rows.append(dict(season=s, reconstructed=round(base[s], 2) if base[s] == base[s] else None,
                         published=k,
                         abs_err=(round(abs(base[s] - k), 2) if k and base[s] == base[s] else None)))
    bl = pd.DataFrame(rows)
    print(bl.to_string(index=False))
    bl.to_csv(US / "baselines.csv", index=False)
    err = bl.abs_err.dropna()
    print(f"validation against published values: max abs error "
          f"{err.max() if len(err) else float('nan'):.2f} pp")

    # ---- precompute smoothed frames
    frames = {}
    cols = list(CHANNELS) + ["percent_positive"]
    for sm in SMOOTH:
        d = d0.copy()
        if sm:
            for c in cols:
                d[c] = d[c].rolling(3, center=True, min_periods=1).mean()
        frames[sm] = d

    specs = list(itertools.product(STAT, NONSEASON, COVID, SMOOTH, SUSTAIN,
                                   REFPERIOD, COMPARATOR, ANCHOR))
    print(f"\n{len(specs)} specifications x {len(CHANNELS)} channels = "
          f"{len(specs)*len(CHANNELS)} estimates")

    out = []
    for i, (stat, nsq, cov, sm, sus, refp, comp, anc) in enumerate(specs):
        d = frames[sm]
        pool_all = d[covid_mask(d, cov)].dropna(subset=["percent_positive"])
        for si, season in enumerate(SEASONS):
            if refp == "rolling3":
                prior = SEASONS[max(0, si - 3):si]
                pool = pool_all[pool_all.season.isin(prior)]
            else:
                pool = pool_all[pool_all.season != season]
            if len(pool) < 20:
                continue
            ns_ref = pool[pool.percent_positive < pool.percent_positive.quantile(nsq)]

            s = d[d.season == season]
            if len(s) < 8:
                continue

            # comparator
            if comp == "ilinet_published":
                ct, cs, cser = base[season], s.dropna(subset=["wili"]), "wili"
            elif comp == "positivity_derived":
                ct = threshold(ns_ref["percent_positive"], "sd1.96")
                cs, cser = s.dropna(subset=["percent_positive"]), "percent_positive"
            else:
                ct = threshold(ns_ref["wili"], "sd1.96")
                cs, cser = s.dropna(subset=["wili"]), "wili"
            if not np.isfinite(ct) or len(cs) < 8:
                continue
            comp_date = first_crossing(cs[cser], cs.MidDate, ct, sus)
            if comp_date is None:
                continue

            for c in CHANNELS:
                if c == cser:          # never compare a series with itself
                    continue
                if anc == "reference_series":
                    thr = threshold(ns_ref[c], stat)
                else:
                    v = pool[c].dropna()
                    thr = threshold(v[v < v.quantile(nsq)], stat) if len(v) >= 20 else np.inf
                sc = s.dropna(subset=[c])
                cd = first_crossing(sc[c], sc.MidDate, thr, sus) if len(sc) >= 8 else None
                out.append(dict(spec_id=i, stat=stat, nonseason_q=nsq, covid=cov,
                                smooth=sm, sustain=sus, refperiod=refp,
                                comparator=comp, anchor=anc, season=season, channel=c,
                                lead_days=(comp_date - cd).days if cd is not None else np.nan))
        if (i + 1) % 500 == 0:
            print(f"  {i+1}/{len(specs)}", flush=True)

    e = pd.DataFrame(out)
    curve = (e.groupby(["spec_id", "stat", "nonseason_q", "covid", "smooth", "sustain",
                        "refperiod", "comparator", "anchor", "channel"], as_index=False)
              .lead_days.median().rename(columns={"lead_days": "median_lead"}))
    curve.to_csv(US / "fluview_speccurve.csv", index=False)
    # Per-season estimates are large and are a working file, not a result.
    e.to_csv(US / "fluview_estimates.csv", index=False)
    pd.set_option("display.width", 250, "display.max_columns", 40)

    c2 = curve[curve.median_lead.notna()]
    dims = ["anchor", "comparator", "covid", "nonseason_q", "stat", "sustain",
            "smooth", "refperiod"]
    print("\n=== SWING BY DIMENSION ===")
    sw = {x: round(float(c2.groupby(x).median_lead.mean().max()
                         - c2.groupby(x).median_lead.mean().min()), 1) for x in dims}
    for k, v in sorted(sw.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<14}{v:>7} d")

    print(f"\nP14 {'CONFIRMED' if sw['anchor'] > sw['comparator'] else 'REFUTED'}: "
          f"anchor {sw['anchor']} d vs comparator {sw['comparator']} d "
          f"({'largest' if sw['anchor']==max(sw.values()) else 'NOT largest'} overall)")

    print("\n=== P15: DIRECTION AND POOLED SIGN ===")
    g = c2.groupby("anchor").median_lead.agg(["mean", "median", "min", "max"]).round(1)
    print(g.to_string())
    own = c2[c2.anchor == "own_series"].median_lead.mean()
    ref = c2[c2.anchor == "reference_series"].median_lead.mean()
    print(f"own minus reference: {own-ref:+.1f} d")
    flip = (np.sign(own) != np.sign(ref))
    print(f"P15 {'CONFIRMED' if (own > ref) else 'REFUTED'} (own longer); "
          f"pooled sign {'REVERSES' if flip else 'does not reverse'} "
          f"({ref:+.1f} -> {own:+.1f})")

    print("\n=== P16: ANCHORING SHIFT AGAINST ZERO INFLATION ===")
    rows2 = []
    for c in CHANNELS:
        v = d0[c].dropna()
        if not len(v):
            continue
        zf = float((v[v <= v.median()] <= 0.05).mean())
        a = c2[(c2.channel == c) & (c2.anchor == "own_series")].median_lead.mean()
        b = c2[(c2.channel == c) & (c2.anchor == "reference_series")].median_lead.mean()
        rows2.append(dict(channel=CHANNELS[c], key=c, zero_frac=round(zf, 3),
                          own=round(a, 1), reference=round(b, 1),
                          anchor_shift=round(a - b, 1)))
    z = pd.DataFrame(rows2).sort_values("anchor_shift", ascending=False)
    print(z.to_string(index=False))
    top = z.iloc[0]
    r, p = st.spearmanr(z.zero_frac, z.anchor_shift)
    print(f"\nlargest anchoring shift: {top.channel} ({top.anchor_shift} d)")
    print(f"Spearman(zero fraction, anchoring shift): rho={r:.3f} p={p:.4f}")
    print(f"P16 {'CONFIRMED' if top.key == 'rate_age_12t17' else 'REFUTED'} "
          f"(predicted rate_age_12t17)")

    print("\n=== P17: SIGN REVERSAL BY CHANNEL ===")
    summ = curve.groupby("channel").median_lead.agg(
        median="median", min="min", max="max",
        pct_positive=lambda v: 100 * (v > 0).mean()).round(1)
    summ["spread"] = (summ["max"] - summ["min"]).round(1)
    summ["label"] = [CHANNELS[c] for c in summ.index]
    print(summ[["label", "median", "min", "max", "spread", "pct_positive"]].to_string())
    fl = curve.groupby("channel").median_lead.agg(
        lambda v: bool((v > 0).any() and (v < 0).any()))
    print(f"\nP17 {'CONFIRMED' if int(fl.sum()) >= 7 else 'REFUTED'}: "
          f"sign reverses in {int(fl.sum())}/{len(fl)} channels (needed >=7 of 10)")

    print("\n=== P18: REFERENCE PERIOD ===")
    rp = c2.groupby("refperiod").median_lead.mean().round(1)
    print(rp.to_string())
    print(f"P18 {'CONFIRMED' if sw['refperiod'] > 5 else 'REFUTED'}: "
          f"swing {sw['refperiod']} d (needed > 5)")


if __name__ == "__main__":
    main()
