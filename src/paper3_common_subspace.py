"""
Analysis B of `paper3_extension_plan.md`: a common-dimension subspace across families.

The manuscript reports that the moving epidemic method is the most stable of three
onset-detection families. That comparison is confounded: MEM's specification space has no
analogue of the non-season-quantile sweep, and the R(t) space varies neither pandemic-era
handling, smoothing, season set nor the sustained rule. Two of the four largest movers in
the threshold family are simply absent from the other two spaces.

This runs all three families over exactly the same five choices, 48 specifications each,
with family-specific parameters pinned at a stated reference value. It answers the
question the full-space analysis cannot: given the same choices, which family moves least.

Shared dimensions (2 x 3 x 2 x 2 x 2 = 48):
    comparator   chp_operational | data_derived
    covid        exclude_2020_2022 | exclude_2020 | include_all
    smooth       none | 3-week centred
    seasonset    all8 | single5
    sustain      1 week | 2 consecutive weeks
"""

import itertools

import numpy as np
import pandas as pd
from scipy import stats

from paper3_common import SEASONS, load_flux

CHANNELS = ["ILI_PMP", "ILI_AED", "ILI_CMP", "ILI_School", "ILI_NonSchool",
            "Fever_RCHE", "Adm_All", "Adm_0_5", "Adm_6_11", "Adm_12_17",
            "Adm_18_49", "Adm_50_64", "Adm_65_higher"]
LABEL = {
    "ILI_PMP": "Outpatient (private GP)", "ILI_AED": "Emergency attendance",
    "ILI_CMP": "Traditional medicine", "ILI_School": "School outbreaks",
    "ILI_NonSchool": "Non-school outbreaks", "Fever_RCHE": "Care-home fever",
    "Adm_All": "Admissions, all ages", "Adm_0_5": "Admissions 0-5y",
    "Adm_6_11": "Admissions 6-11y", "Adm_12_17": "Admissions 12-17y",
    "Adm_18_49": "Admissions 18-49y", "Adm_50_64": "Admissions 50-64y",
    "Adm_65_higher": "Admissions 65+y",
}
CHP_OPERATIONAL = 0.0494
SINGLE_WAVE = ["2014/15 winter", "2015/16 winter", "2018/19 winter",
               "2023 summer", "2024/25 winter"]

# ---- pinned family-specific reference parameters (stated, not varied) --------
THR_STAT, THR_NSQ, THR_ANCHOR = "sd1.96", 0.40, "reference_series"
MEM_N, MEM_MEAN, MEM_CONF, MEM_PERIODS = 5, "arithmetic", 0.95, "pre_only"
RT_SI_MEAN, RT_SI_SD, RT_WINDOW, RT_PRIOR, RT_SCALE, RT_RULE = \
    3.0, 2.0, 3, (1.0, 0.2), 1e4, "posterior_mean"
MAX_LAG = 4

df_raw = load_flux()


def covid_mask(d, mode):
    if mode == "exclude_2020_2022":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2022-12-31"))
    if mode == "exclude_2020":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2020-12-31"))
    return pd.Series(True, index=d.index)


def first_crossing(series, dates, thr, sustain):
    above = (np.asarray(series, dtype=float) > thr)
    for i in range(len(above) - sustain + 1):
        if above[i:i + sustain].all():
            return dates.iloc[i]
    return None


def si_weights(mean_d, sd_d, max_lag=MAX_LAG):
    shape = (mean_d / sd_d) ** 2
    scale = sd_d ** 2 / mean_d
    edges = np.arange(0, (max_lag + 1) * 7 + 1, 7)
    w = np.diff(stats.gamma.cdf(edges, a=shape, scale=scale))
    return w / w.sum() if w.sum() > 0 else np.ones(max_lag) / max_lag


W = si_weights(RT_SI_MEAN, RT_SI_SD)


def rt_onset(inc_raw, dates, window, a, b, sustain):
    """First date the posterior mean R exceeds 1 for `sustain` consecutive weeks."""
    inc = np.asarray(inc_raw, dtype=float)
    n = len(inc)
    lam = np.zeros(n)
    for k, wk in enumerate(W, start=1):
        if k < n:
            lam[k:] += inc[:-k] * wk
    flags = np.zeros(n, dtype=bool)
    for t in range(window, n):
        sl = slice(t - window + 1, t + 1)
        shape, rate = a + inc[sl].sum(), 1.0 / b + lam[sl].sum()
        if rate > 0 and shape > 0:
            flags[t] = (shape / rate) > 1.0
    for i in range(n - sustain + 1):
        if flags[i:i + sustain].all():
            return dates.iloc[i]
    return None


def nonepidemic(s, ch):
    v = s[ch].dropna()
    if len(v) < 8:
        return np.array([])
    peak = int(np.argmax(v.values))
    return v.values[np.arange(len(v)) < max(peak - 2, 0)]


def mem_threshold(vals, n, conf):
    if len(vals) < 3:
        return np.inf
    top = np.sort(vals)[-n:] if len(vals) >= n else np.sort(vals)
    if len(top) < 2:
        return np.inf
    m, sd = top.mean(), top.std(ddof=1)
    if sd == 0 or np.isnan(sd):
        return float(m)
    return float(m + stats.t.ppf(conf, df=len(top) - 1) * sd / np.sqrt(len(top)))


def run_common(comparator, covid, smooth, seasonset, sustain):
    """Return {(family, channel): median_lead} for one shared specification."""
    d = df_raw.copy()
    cols = CHANNELS + ["AandB_proportion"]
    if smooth:
        for c in cols:
            d[c] = d[c].rolling(3, center=True, min_periods=1).mean()

    pool = d[covid_mask(d, covid)].dropna(subset=["AandB_proportion"])
    ns = pool[pool.AandB_proportion < pool.AandB_proportion.quantile(THR_NSQ)]
    comp_thr = (CHP_OPERATIONAL if comparator == "chp_operational"
                else float(ns.AandB_proportion.mean() + 1.96 * ns.AandB_proportion.std()))
    thr_by_ch = {c: (ns[c].dropna().mean() + 1.96 * ns[c].dropna().std())
                 if ns[c].notna().sum() >= 5 else np.inf for c in CHANNELS}

    names = SINGLE_WAVE if seasonset == "single5" else [s[0] for s in SEASONS]
    sl = {}
    for name, start, end in SEASONS:
        s = d[(d.MidDate >= start) & (d.MidDate <= end)].dropna(subset=["AandB_proportion"])
        if len(s) >= 12:
            sl[name] = s

    a, b = RT_PRIOR
    per = {(f, c): [] for f in ("threshold", "mem", "rt") for c in CHANNELS}
    for name in names:
        if name not in sl:
            continue
        s = sl[name]
        comp_date = first_crossing(s.AandB_proportion, s.MidDate, comp_thr, sustain)
        if comp_date is None:
            continue
        # MEM trains leave-one-out on the other eligible seasons
        train = [m for m in sl if m != name and
                 covid_mask(sl[m].iloc[[0]], covid).iloc[0]]
        for c in CHANNELS:
            sc = s.dropna(subset=[c])
            if len(sc) < 8:
                continue
            cd = first_crossing(sc[c], sc.MidDate, thr_by_ch[c], sustain)
            if cd is not None:
                per[("threshold", c)].append((comp_date - cd).days)

            vals = np.concatenate([nonepidemic(sl[m], c) for m in train]) if train \
                else np.array([])
            if len(vals) >= 3:
                md = first_crossing(sc[c], sc.MidDate,
                                    mem_threshold(vals, MEM_N * len(train), MEM_CONF), sustain)
                if md is not None:
                    per[("mem", c)].append((comp_date - md).days)

            rd = rt_onset(np.round(sc[c].values.astype(float) * RT_SCALE),
                          sc.MidDate, RT_WINDOW, a, b, sustain)
            if rd is not None:
                per[("rt", c)].append((comp_date - rd).days)

    return {k: (float(np.median(v)) if v else np.nan) for k, v in per.items()}


COMPARATOR = ["chp_operational", "data_derived"]
COVID = ["exclude_2020_2022", "exclude_2020", "include_all"]
SMOOTH = [False, True]
SEASONSET = ["all8", "single5"]
SUSTAIN = [1, 2]

specs = list(itertools.product(COMPARATOR, COVID, SMOOTH, SEASONSET, SUSTAIN))
print(f"{len(specs)} shared specifications x 3 families x {len(CHANNELS)} channels",
      flush=True)

rows = []
for i, sp in enumerate(specs):
    tag = dict(zip(["comparator", "covid", "smooth", "seasonset", "sustain"], sp))
    res = run_common(*sp)
    for (fam, ch), val in res.items():
        rows.append({**tag, "spec_id": i, "family": fam, "channel": ch, "median_lead": val})
    print(f"  {i+1}/{len(specs)}", flush=True)

curve = pd.DataFrame(rows)
curve.to_csv("paper3_common_subspace.csv", index=False)

pd.set_option("display.width", 250, "display.max_columns", 40)
print("\n=== P6: SPREAD BY FAMILY ON THE COMMON SUBSPACE ===")
out = []
for fam in ("threshold", "mem", "rt"):
    f = curve[curve.family == fam]
    per = f.groupby("channel").median_lead.agg(
        spread=lambda v: (v.max() - v.min()) if v.notna().any() else np.nan,
        pct_pos=lambda v: 100 * (v > 0).mean())
    flips = f.groupby("channel").median_lead.agg(
        lambda v: bool((v > 0).any() and (v < 0).any())).sum()
    out.append({"family": fam, "median_spread": round(per.spread.median(), 1),
                "min_spread": round(per.spread.min(), 1),
                "max_spread": round(per.spread.max(), 1),
                "sign_flips": f"{int(flips)}/13"})
o = pd.DataFrame(out)
print(o.to_string(index=False))

thr_s = o.loc[o.family == "threshold", "median_spread"].iloc[0]
mem_s = o.loc[o.family == "mem", "median_spread"].iloc[0]
rt_s = o.loc[o.family == "rt", "median_spread"].iloc[0]
ratio = thr_s / mem_s if mem_s else np.inf
print(f"\nfull-space ratio threshold/MEM was 140/45.5 = 3.08")
print(f"common-subspace ratio threshold/MEM = {thr_s}/{mem_s} = {ratio:.2f}")
print(f"P6 {'CONFIRMED' if ratio < 1.55 else 'REFUTED'} "
      f"(predicted the ratio falls below 1.55)")
print(f"P7 {'CONFIRMED' if rt_s >= max(thr_s, mem_s) else 'REFUTED'} "
      f"(R(t) widest: {rt_s} vs threshold {thr_s}, MEM {mem_s})")

thr_flips = int(curve[curve.family == "threshold"].groupby("channel").median_lead.agg(
    lambda v: bool((v > 0).any() and (v < 0).any())).sum())
print(f"P8 {'CONFIRMED' if thr_flips >= 7 else 'REFUTED'} "
      f"(threshold sign reverses in {thr_flips}/13 channels)")

print("\n=== PER-CHANNEL SPREAD, ALL THREE FAMILIES ===")
piv = curve.pivot_table(index="channel", columns="family", values="median_lead",
                        aggfunc=lambda v: v.max() - v.min())
piv["label"] = [LABEL[c] for c in piv.index]
print(piv[["label", "threshold", "mem", "rt"]].round(1).to_string())
