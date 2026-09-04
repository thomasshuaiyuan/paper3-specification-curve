"""
Analysis A of `paper3_extension_plan.md`: baseline anchoring as an eighth dimension.

The seven existing dimensions are all tuning choices. Anchoring is structural: it
decides which weeks the baseline is computed from at all.

  reference_series -- non-season weeks are those where influenza POSITIVITY is below
                      quantile q; every channel is then read on that same set of weeks.
  own_series       -- non-season weeks are those where THAT CHANNEL is below its own
                      quantile q. Every channel gets a different set of weeks.

The second is the convention used in `preonset_analysis.py` for the v8 manuscript. It
inherits each channel's zero fraction into its threshold, so a zero-inflated series gets
a structurally lower bar. That is what put 12-17y admissions first in 3 of 5 seasons.

864 x 2 = 1,728 specifications x 13 channels.
"""

import itertools

import numpy as np
import pandas as pd

from paper3_common import SEASONS, load_flux

CHANNELS = {
    "ILI_PMP": "Outpatient (private GP)", "ILI_AED": "Emergency attendance",
    "ILI_CMP": "Traditional medicine", "ILI_School": "School outbreaks",
    "ILI_NonSchool": "Non-school outbreaks", "Fever_RCHE": "Care-home fever",
    "Adm_All": "Admissions, all ages", "Adm_0_5": "Admissions 0-5y",
    "Adm_6_11": "Admissions 6-11y", "Adm_12_17": "Admissions 12-17y",
    "Adm_18_49": "Admissions 18-49y", "Adm_50_64": "Admissions 50-64y",
    "Adm_65_higher": "Admissions 65+y",
}

CHP_OPERATIONAL = 0.0494
STAT = ["sd1.645", "sd1.96", "sd2.58", "p90", "p95", "p97.5"]
NONSEASON = [0.25, 0.40, 0.50]
COVID = ["exclude_2020_2022", "exclude_2020", "include_all"]
SMOOTH = [False, True]
SUSTAIN = [1, 2]
SEASONSET = ["all8", "single5"]
COMPARATOR = ["chp_operational", "data_derived"]
ANCHOR = ["reference_series", "own_series"]          # the new dimension
SINGLE_WAVE = ["2014/15 winter", "2015/16 winter", "2018/19 winter",
               "2023 summer", "2024/25 winter"]

df_raw = load_flux()


def covid_mask(d, mode):
    if mode == "exclude_2020_2022":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2022-12-31"))
    if mode == "exclude_2020":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2020-12-31"))
    return pd.Series(True, index=d.index)


def threshold(values, stat):
    v = pd.Series(values).dropna()
    if len(v) < 5:
        return np.inf
    if stat.startswith("sd"):
        return v.mean() + float(stat[2:]) * v.std()
    return v.quantile(float(stat[1:]) / 100.0)


def first_crossing(series, dates, thr, sustain):
    above = (series > thr).values
    for i in range(len(above) - sustain + 1):
        if above[i:i + sustain].all():
            return dates.iloc[i]
    return None


def run_spec(stat, nsq, covid, smooth, sustain, seasonset, comparator, anchor):
    d = df_raw.copy()
    cols = list(CHANNELS) + ["AandB_proportion"]
    if smooth:
        for c in cols:
            d[c] = d[c].rolling(3, center=True, min_periods=1).mean()

    pool = d[covid_mask(d, covid)].dropna(subset=["AandB_proportion"])

    # comparator threshold is always positivity-based; anchoring applies to the channels
    ns_ref = pool[pool.AandB_proportion < pool.AandB_proportion.quantile(nsq)]
    comp_thr = (CHP_OPERATIONAL if comparator == "chp_operational"
                else threshold(ns_ref["AandB_proportion"], "sd1.96"))

    ch_thr = {}
    for c in CHANNELS:
        if anchor == "reference_series":
            ch_thr[c] = threshold(ns_ref[c], stat)
        else:
            v = pool[c].dropna()
            ch_thr[c] = threshold(v[v < v.quantile(nsq)], stat) if len(v) >= 20 else np.inf

    seasons = SINGLE_WAVE if seasonset == "single5" else [s[0] for s in SEASONS]
    out = []
    for name, start, end in SEASONS:
        if name not in seasons:
            continue
        s = d[(d.MidDate >= start) & (d.MidDate <= end)].dropna(subset=["AandB_proportion"])
        if len(s) < 8:
            continue
        comp_date = first_crossing(s.AandB_proportion, s.MidDate, comp_thr, sustain)
        if comp_date is None:
            continue
        for c in CHANNELS:
            sc = s.dropna(subset=[c])
            cd = first_crossing(sc[c], sc.MidDate, ch_thr[c], sustain) if len(sc) >= 8 else None
            out.append({"season": name, "channel": c,
                        "lead_days": (comp_date - cd).days if cd is not None else np.nan})
    return out


specs = list(itertools.product(STAT, NONSEASON, COVID, SMOOTH, SUSTAIN,
                               SEASONSET, COMPARATOR, ANCHOR))
print(f"{len(specs)} specifications x {len(CHANNELS)} channels", flush=True)

rows = []
for i, sp in enumerate(specs):
    tag = dict(zip(["stat", "nonseason_q", "covid", "smooth", "sustain",
                    "seasonset", "comparator", "anchor"], sp))
    res = pd.DataFrame(run_spec(*sp))
    for c in CHANNELS:
        v = res[res.channel == c].lead_days.dropna()
        rows.append({**tag, "spec_id": i, "channel": c, "n_seasons": len(v),
                     "median_lead": float(v.median()) if len(v) else np.nan})
    if (i + 1) % 200 == 0:
        print(f"  {i+1}/{len(specs)}", flush=True)

curve = pd.DataFrame(rows)
curve.to_csv("paper3_anchor_speccurve.csv", index=False)
pd.set_option("display.width", 250, "display.max_columns", 40)

print("\n=== P5: SWING BY DIMENSION, ANCHORING INCLUDED ===")
c2 = curve[curve.median_lead.notna()]
dims = ["anchor", "comparator", "covid", "nonseason_q", "stat", "sustain", "smooth", "seasonset"]
sw = {d: round(float(c2.groupby(d).median_lead.mean().max()
                     - c2.groupby(d).median_lead.mean().min()), 1) for d in dims}
for k, v in sorted(sw.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<14}{v:>7} d")
print(f"\nP5 {'CONFIRMED' if sw['anchor'] > sw['comparator'] else 'REFUTED'}: "
      f"anchor {sw['anchor']} d vs comparator {sw['comparator']} d")

print("\n=== P9: DIRECTION OF THE ANCHORING EFFECT ===")
print(c2.groupby("anchor").median_lead.agg(["mean", "median", "min", "max"]).round(1).to_string())
diff = (c2[c2.anchor == "own_series"].median_lead.mean()
        - c2[c2.anchor == "reference_series"].median_lead.mean())
print(f"own_series minus reference_series: {diff:+.1f} d")
print(f"P9 {'CONFIRMED' if diff > 0 else 'REFUTED'} (predicted own_series longer)")

print("\n=== ANCHORING EFFECT BY CHANNEL, AGAINST ZERO FRACTION ===")
rows2 = []
for c in CHANNELS:
    v = df_raw[c].dropna()
    zf = (v[v <= v.median()] == 0).mean()
    a = c2[(c2.channel == c) & (c2.anchor == "own_series")].median_lead.mean()
    b = c2[(c2.channel == c) & (c2.anchor == "reference_series")].median_lead.mean()
    rows2.append({"channel": CHANNELS[c], "zero_frac": round(zf, 3),
                  "own": round(a, 1), "reference": round(b, 1), "anchor_shift": round(a - b, 1)})
z = pd.DataFrame(rows2).sort_values("zero_frac", ascending=False)
print(z.to_string(index=False))
from scipy import stats as st
r, p = st.spearmanr(z.zero_frac, z["anchor_shift"])
print(f"\nSpearman(zero fraction, anchoring shift): rho={r:.3f}  p={p:.4f}")

print("\n=== DISPERSION BY CHANNEL, FULL 1,728-SPEC SPACE ===")
summ = curve.groupby("channel").median_lead.agg(
    median="median", min="min", max="max",
    pct_positive=lambda v: 100 * (v > 0).mean()).round(1)
summ["spread"] = (summ["max"] - summ["min"]).round(1)
summ["label"] = [CHANNELS[c] for c in summ.index]
print(summ[["label", "median", "min", "max", "spread", "pct_positive"]].to_string())
flip = curve.groupby("channel").median_lead.agg(lambda v: (v > 0).any() and (v < 0).any())
print(f"\nsign reverses in {int(flip.sum())}/{len(flip)} channels "
      f"(was 12/13 on the 864-spec space)")
