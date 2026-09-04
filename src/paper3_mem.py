"""
Paper 3, third family: the moving epidemic method (MEM).

MEM is the threshold method used by ECDC and many national influenza systems,
so a reader can reasonably object that our first two families are not what they
use. This applies the same treatment to MEM.

The algorithm, as described across published applications:

  1. From historical seasons, identify the non-epidemic weeks.
  2. Take the n highest values from those weeks in each season.
  3. Compute the mean of the pooled values.
  4. The pre-epidemic threshold is the upper limit of a one-sided confidence
     interval around that mean.
  5. Epidemic onset in the target season is the first week the observation
     exceeds the threshold, optionally sustained.

Published descriptions disagree on the details, and those disagreements are
exactly what we cross:

  - arithmetic or geometric mean of the selected values
  - how many values per season (n)
  - confidence level 90%, 95% or 99%
  - one week above threshold, or two consecutive
  - non-epidemic weeks drawn from before the peak only, or before and after
  - which historical seasons are eligible (pandemic-era handling)
  - which comparator the onset is measured against

7 dimensions, 576 specifications per channel.

SIMPLIFICATION, stated plainly: the full method selects the epidemic period by
an iterative MAP-curve procedure. We instead define the epidemic period of a
training season as the weeks within +/-2 of that season's peak, and draw
non-epidemic values from outside it. This is a transparent approximation, not
the `mem` R package, and is reported as such.
"""

import itertools

import numpy as np
import pandas as pd
from scipy import stats

from paper3_common import SEASONS, load_flux

CHANNELS = ["ILI_PMP", "ILI_AED", "ILI_CMP", "ILI_School", "ILI_NonSchool",
            "Fever_RCHE", "Adm_All", "Adm_0_5", "Adm_6_11", "Adm_12_17",
            "Adm_18_49", "Adm_50_64", "Adm_65_higher"]
CHP_OPERATIONAL = 0.0494

N_POINTS = [3, 5, 8, 12]
MEAN_TYPE = ["arithmetic", "geometric"]
CONF = [0.90, 0.95, 0.99]
CONSEC = [1, 2]
PERIODS = ["pre_only", "pre_and_post"]
COVID = ["exclude_2020_2022", "exclude_2020", "include_all"]
COMPARATOR = ["chp_operational", "data_derived"]

df_raw = load_flux()
SEASON_LIST = [(n, s, e) for n, s, e in SEASONS]

# slice seasons once
SD = {}
for name, start, end in SEASON_LIST:
    s = df_raw[(df_raw.MidDate >= start) & (df_raw.MidDate <= end)].dropna(
        subset=["AandB_proportion"]).reset_index(drop=True)
    if len(s) >= 12:
        SD[name] = s

# comparator crossing dates
pool = df_raw[~((df_raw.MidDate >= "2020-01-01") & (df_raw.MidDate <= "2022-12-31"))]
pool = pool.dropna(subset=["AandB_proportion"])
ns_pool = pool[pool.AandB_proportion < pool.AandB_proportion.median()]
DERIVED = float(ns_pool.AandB_proportion.mean() + 1.96 * ns_pool.AandB_proportion.std())
COMP = {}
for name, s in SD.items():
    for cn, thr in [("chp_operational", CHP_OPERATIONAL), ("data_derived", DERIVED)]:
        hit = s[s.AandB_proportion > thr]
        COMP[(name, cn)] = hit.iloc[0].MidDate if len(hit) else None

# pandemic-era eligibility of each season, by handling mode
def eligible(name, mode):
    _, start, _ = next(x for x in SEASON_LIST if x[0] == name)
    y = pd.Timestamp(start).year
    if mode == "exclude_2020_2022":
        return not (2020 <= y <= 2022)
    if mode == "exclude_2020":
        return y != 2020
    return True


def nonepidemic_values(s, ch, periods):
    """Values outside the epidemic period, defined as +/-2 weeks around the peak."""
    v = s[ch].dropna()
    if len(v) < 8:
        return np.array([])
    peak = int(np.argmax(v.values))
    idx = np.arange(len(v))
    if periods == "pre_only":
        keep = idx < max(peak - 2, 0)
    else:
        keep = (idx < max(peak - 2, 0)) | (idx > min(peak + 2, len(v) - 1))
    return v.values[keep]


def mem_threshold(vals, n, mean_type, conf):
    """Upper limit of a one-sided CI around the mean of the n highest values."""
    if len(vals) < 3:
        return np.inf
    top = np.sort(vals)[-n:] if len(vals) >= n else np.sort(vals)
    top = top[top > 0] if mean_type == "geometric" else top
    if len(top) < 2:
        return np.inf
    if mean_type == "geometric":
        x = np.log(top)
    else:
        x = top
    m, sd = x.mean(), x.std(ddof=1)
    if sd == 0 or np.isnan(sd):
        return float(np.exp(m)) if mean_type == "geometric" else float(m)
    se = sd / np.sqrt(len(x))
    tcrit = stats.t.ppf(conf, df=len(x) - 1)
    up = m + tcrit * se
    return float(np.exp(up)) if mean_type == "geometric" else float(up)


def first_cross(s, ch, thr, consec):
    v = s.dropna(subset=[ch])
    above = (v[ch] > thr).values
    for i in range(len(above) - consec + 1):
        if above[i:i + consec].all():
            return v.MidDate.iloc[i]
    return None


specs = list(itertools.product(N_POINTS, MEAN_TYPE, CONF, CONSEC, PERIODS, COVID, COMPARATOR))
print(f"{len(specs)} MEM specifications x {len(CHANNELS)} channels", flush=True)

rows = []
for i, (n, mt, conf, consec, periods, covid, cmp_name) in enumerate(specs):
    tag = dict(n_points=n, mean_type=mt, conf=conf, consecutive=consec,
               periods=periods, covid=covid, comparator=cmp_name)
    per = {c: [] for c in CHANNELS}
    for target in SD:
        comp_date = COMP[(target, cmp_name)]
        if comp_date is None:
            continue
        # leave-one-out: threshold from every other eligible season
        train = [m for m in SD if m != target and eligible(m, covid)]
        if not train:
            continue
        for ch in CHANNELS:
            vals = np.concatenate([nonepidemic_values(SD[m], ch, periods) for m in train]) \
                if train else np.array([])
            if len(vals) < 3:
                continue
            thr = mem_threshold(vals, n * len(train), mt, conf)
            cd = first_cross(SD[target], ch, thr, consec)
            if cd is not None:
                per[ch].append((comp_date - cd).days)
    for ch in CHANNELS:
        v = per[ch]
        rows.append({**tag, "spec_id": i, "channel": ch, "n_detected": len(v),
                     "median_lead": float(np.median(v)) if v else np.nan})
    if (i + 1) % 100 == 0:
        print(f"  {i+1}/{len(specs)}", flush=True)

curve = pd.DataFrame(rows)
curve.to_csv("paper3_mem_speccurve.csv", index=False)

pd.set_option("display.width", 250, "display.max_columns", 40)
print("\n=== MEM: DISPERSION BY CHANNEL ===")
summ = curve.groupby("channel").median_lead.agg(
    median="median", min="min", max="max",
    pct_positive=lambda v: 100 * (v > 0).mean(),
    n_na=lambda v: v.isna().sum()).round(1)
summ["spread"] = (summ["max"] - summ["min"]).round(1)
print(summ.to_string())

flip = curve.groupby("channel").median_lead.agg(lambda v: (v > 0).any() and (v < 0).any())
print(f"\nsign reverses in {int(flip.sum())}/{len(flip)} channels")
print(f"spread range: {summ.spread.min():.0f} to {summ.spread.max():.0f} days")

print("\n=== WHICH MEM CHOICE DOMINATES ===")
c2 = curve[curve.median_lead.notna()]
sw = {d: round(float(c2.groupby(d).median_lead.mean().max()
                     - c2.groupby(d).median_lead.mean().min()), 1)
      for d in ["comparator", "n_points", "mean_type", "conf", "consecutive", "periods", "covid"]}
for k, v in sorted(sw.items(), key=lambda kv: -kv[1]):
    print(f"  {k:<12}{v:>7} d")

print("\n=== THREE FAMILIES SIDE BY SIDE (% of specifications with a positive lead) ===")
thr = pd.read_csv("paper3_anchor_speccurve.csv")
rt = pd.read_csv("paper3_rt_speccurve.csv")
for ch in CHANNELS:
    a = thr[thr.channel == ch].median_lead.dropna()
    b = rt[rt.channel == ch].median_lead.dropna()
    m = curve[curve.channel == ch].median_lead.dropna()
    print(f"  {ch:<15} threshold {100*(a>0).mean():>5.1f}%   "
          f"R(t) {100*(b>0).mean():>5.1f}%   MEM {100*(m>0).mean():>5.1f}%")
