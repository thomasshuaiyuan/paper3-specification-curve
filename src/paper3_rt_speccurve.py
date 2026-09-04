"""
Paper 3, second extension: does R(t)-based onset detection escape the problem?

The threshold-crossing analysis is open to the objection "we do not use
thresholds, we estimate R(t)". This applies the same treatment to R(t)-based
onset, using the Cori et al. (2013) renewal-equation posterior implemented
directly so every specification choice is explicit.

Posterior for R over a window tau ending at t, with prior R ~ Gamma(a, scale=b):

    shape = a + sum_{s in tau} I_s
    rate  = 1/b + sum_{s in tau} Lambda_s ,   Lambda_s = sum_k I_{s-k} w_k

Onset is the first week the chosen criterion holds. Note that multiplying the
incidence proxy by a constant c scales both sums, so the posterior is NOT
scale-invariant: as c grows the prior washes out. v7's own methods flag this
(degenerate R(t) maxima above 100,000 from a Gamma(0.001, 0.001) prior on
differently-scaled pseudo-counts). Scaling is therefore included as an explicit
specification dimension rather than a footnote.

Seven dimensions, 864 specifications, matching the threshold analysis exactly
so the two are directly comparable.
"""

import itertools

import numpy as np
import pandas as pd
from scipy import stats

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

SI_MEAN = [2.0, 3.0, 4.0]        # days; influenza serial interval range
SI_SD = [1.0, 2.0]               # days
WINDOW = [2, 3, 4, 6]            # weeks
PRIOR = [("v7", 1.0, 0.2), ("vague", 0.001, 0.001), ("weak_wide", 1.0, 5.0)]
SCALING = [1e3, 1e4, 1e5]        # incidence proxy multiplier
ONSET_RULE = ["posterior_mean", "ci_lower"]
COMPARATOR = ["chp_operational", "data_derived"]

MAX_LAG = 4                      # weekly lags retained in the SI


def si_weights(mean_d, sd_d, max_lag=MAX_LAG):
    """Discretise a gamma serial interval (days) onto weekly lags 1..max_lag."""
    shape = (mean_d / sd_d) ** 2
    scale = sd_d ** 2 / mean_d
    edges = np.arange(0, (max_lag + 1) * 7 + 1, 7)          # 0,7,14,...
    cdf = stats.gamma.cdf(edges, a=shape, scale=scale)
    w = np.diff(cdf)                                         # mass in each week
    if w.sum() <= 0:
        w = np.ones(max_lag) / max_lag
    return w / w.sum()


def lambda_series(inc, w):
    """Total infectiousness Lambda_t = sum_k I_{t-k} w_k."""
    n = len(inc)
    lam = np.zeros(n)
    for k, wk in enumerate(w, start=1):
        if k < n:
            lam[k:] += inc[:-k] * wk
    return lam


def rt_onset(inc_raw, dates, w, window, a, b, rule):
    """First week the onset criterion holds; None if never."""
    inc = np.asarray(inc_raw, dtype=float)
    lam = lambda_series(inc, w)
    n = len(inc)
    for t in range(window, n):
        sl = slice(t - window + 1, t + 1)
        shape = a + inc[sl].sum()
        rate = 1.0 / b + lam[sl].sum()
        if rate <= 0 or shape <= 0:
            continue
        if rule == "posterior_mean":
            val = shape / rate
        else:
            val = stats.gamma.ppf(0.025, a=shape, scale=1.0 / rate)
        if val > 1.0:
            return dates.iloc[t]
    return None


df_raw = load_flux()
seasons = [(n, s, e) for n, s, e in SEASONS]

# Pre-slice each season once
season_data = {}
for name, start, end in seasons:
    s = df_raw[(df_raw.MidDate >= start) & (df_raw.MidDate <= end)].dropna(
        subset=["AandB_proportion"]).reset_index(drop=True)
    if len(s) >= 12:
        season_data[name] = s

# Data-derived comparator threshold (fixed, computed once from non-season weeks)
pool = df_raw[~((df_raw.MidDate >= "2020-01-01") & (df_raw.MidDate <= "2022-12-31"))]
pool = pool.dropna(subset=["AandB_proportion"])
ns = pool[pool.AandB_proportion < pool.AandB_proportion.median()]
DERIVED = float(ns.AandB_proportion.mean() + 1.96 * ns.AandB_proportion.std())
print(f"data-derived comparator threshold: {DERIVED*100:.2f}%   "
      f"operational: {CHP_OPERATIONAL*100:.2f}%", flush=True)

# Comparator crossing dates (threshold on positivity, as in the primary analysis)
COMP = {}
for name, s in season_data.items():
    for cmp_name, thr in [("chp_operational", CHP_OPERATIONAL), ("data_derived", DERIVED)]:
        hit = s[s.AandB_proportion > thr]
        COMP[(name, cmp_name)] = hit.iloc[0].MidDate if len(hit) else None

# Pre-compute weights once per SI
W = {(m, sd): si_weights(m, sd) for m in SI_MEAN for sd in SI_SD}
print("SI weight vectors (weekly lags 1-4):")
for k, v in W.items():
    print(f"  mean {k[0]} sd {k[1]}: " + " ".join(f"{x:.3f}" for x in v))

specs = list(itertools.product(SI_MEAN, SI_SD, WINDOW, PRIOR, SCALING, ONSET_RULE, COMPARATOR))
print(f"\n{len(specs)} specifications x {len(CHANNELS)} channels", flush=True)

rows = []
for i, (m, sd, win, (pname, a, b), sc, rule, cmp_name) in enumerate(specs):
    w = W[(m, sd)]
    tag = {"si_mean": m, "si_sd": sd, "window": win, "prior": pname,
           "scaling": sc, "onset_rule": rule, "comparator": cmp_name}
    per = {c: [] for c in CHANNELS}
    for name, s in season_data.items():
        comp_date = COMP[(name, cmp_name)]
        if comp_date is None:
            continue
        for c in CHANNELS:
            sc_df = s.dropna(subset=[c])
            if len(sc_df) < 12:
                continue
            inc = np.round(sc_df[c].values.astype(float) * sc)
            od = rt_onset(inc, sc_df.MidDate, w, win, a, b, rule)
            if od is not None:
                per[c].append((comp_date - od).days)
    for c in CHANNELS:
        v = per[c]
        rows.append({**tag, "spec_id": i, "channel": c,
                     "n_detected": len(v),
                     "median_lead": float(np.median(v)) if v else np.nan})
    if (i + 1) % 150 == 0:
        print(f"  {i+1}/{len(specs)}", flush=True)

curve = pd.DataFrame(rows)
curve.to_csv("paper3_rt_speccurve.csv", index=False)

pd.set_option("display.width", 250, "display.max_columns", 40)
print("\n=== R(t)-BASED ONSET: DISPERSION BY CHANNEL (864 specifications) ===")
summ = curve.groupby("channel").median_lead.agg(
    median="median", min="min", max="max",
    pct_positive=lambda v: 100 * (v > 0).mean(),
    n_na=lambda v: v.isna().sum()).round(1)
summ["spread"] = (summ["max"] - summ["min"]).round(1)
summ["label"] = [CHANNELS[c] for c in summ.index]
print(summ[["label", "median", "min", "max", "spread", "pct_positive", "n_na"]].to_string())

flip = curve.groupby("channel").median_lead.agg(lambda v: (v > 0).any() and (v < 0).any())
print(f"\nchannels where the sign reverses: {int(flip.sum())}/{len(flip)}")
print(f"spread range: {summ.spread.min():.0f} to {summ.spread.max():.0f} days")

print("\n=== WHICH CHOICE DOMINATES (swing in mean median-lead, pooled) ===")
c2 = curve[curve.median_lead.notna()]
sw = {d: round(float(c2.groupby(d).median_lead.mean().max()
                     - c2.groupby(d).median_lead.mean().min()), 1)
      for d in ["comparator", "scaling", "prior", "window", "onset_rule", "si_mean", "si_sd"]}
for k, v in sorted(sw.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<12}{v:>7} d")

print("\n=== THE SCALING EFFECT (v7 flags this; here it is quantified) ===")
print(c2.groupby("scaling").median_lead.agg(["mean", "median", "min", "max"]).round(1).to_string())
print("\nby prior x scaling (mean median-lead):")
print(c2.pivot_table(index="prior", columns="scaling", values="median_lead",
                     aggfunc="mean").round(1).to_string())
