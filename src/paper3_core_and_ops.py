"""
Two robustness additions to Paper 3.

(1) CORE SPECIFICATION SET.
    The headline range treats all 864 specifications as equally defensible.
    Some corners are individually reasonable but jointly odd: retaining
    pandemic weeks in the baseline AND using the most permissive non-season
    window AND the lowest threshold is a combination no analyst would choose
    deliberately. We define a pre-stated "core" subset by excluding
    combinations that stack permissive choices, and report the range within it.
    If the finding survives on the core set it is not an artifact of extremes.

(2) OPERATIONAL CONSEQUENCE.
    Statistical spread only matters if it changes what an agency would do.
    For each season we find the earliest and latest onset declaration date
    produced by any core specification, and express the gap in weeks of
    preparedness time.
"""

import numpy as np
import pandas as pd

curve = pd.read_csv("paper3_anchor_speccurve.csv")
LABEL = {
    "ILI_PMP": "Outpatient (private GP)", "ILI_AED": "Emergency attendance",
    "ILI_CMP": "Traditional medicine", "ILI_School": "School outbreaks",
    "ILI_NonSchool": "Non-school outbreaks", "Fever_RCHE": "Care-home fever",
    "Adm_All": "Admissions, all ages", "Adm_0_5": "Admissions 0-5y",
    "Adm_6_11": "Admissions 6-11y", "Adm_12_17": "Admissions 12-17y",
    "Adm_18_49": "Admissions 18-49y", "Adm_50_64": "Admissions 50-64y",
    "Adm_65_higher": "Admissions 65+y",
}

# ---------------------------------------------------------------- (1) core set
# Permissive = makes crossing easier / lead look longer.
PERMISSIVE = {
    "covid": "include_all",          # pandemic weeks depress the baseline
    "nonseason_q": 0.25,             # narrowest non-season window
    "stat": "p90",                   # lowest threshold
    "comparator": "chp_operational",  # most generous comparator
}
STRICT = {
    "covid": "exclude_2020_2022",
    "nonseason_q": 0.50,
    "stat": "p97.5",
    "comparator": "data_derived",
}


def n_extreme(row, table):
    return sum(row[k] == v for k, v in table.items())


curve["n_permissive"] = curve.apply(lambda r: n_extreme(r, PERMISSIVE), axis=1)
curve["n_strict"] = curve.apply(lambda r: n_extreme(r, STRICT), axis=1)
# core = at most two of the four extreme choices stacked in either direction
curve["core"] = (curve.n_permissive <= 2) & (curve.n_strict <= 2)

print(f"core subset: {curve.core.sum() // len(LABEL)} of "
      f"{len(curve) // len(LABEL)} specifications retained "
      f"({100*curve.core.mean():.0f}%)")

rows = []
for ch in LABEL:
    a = curve[(curve.channel == ch)].median_lead.dropna()
    c = curve[(curve.channel == ch) & curve.core].median_lead.dropna()
    rows.append({"channel": LABEL[ch],
                 "full_range": f"{a.min():.0f} to {a.max():.0f}",
                 "full_spread": a.max() - a.min(),
                 "core_range": f"{c.min():.0f} to {c.max():.0f}",
                 "core_spread": c.max() - c.min(),
                 "core_sign_flips": bool((c > 0).any() and (c < 0).any()),
                 "core_pct_pos": round(100 * (c > 0).mean(), 1)})
d = pd.DataFrame(rows)
pd.set_option("display.width", 240)
print("\n=== FULL vs CORE SPECIFICATION SET ===")
print(d.to_string(index=False))
print(f"\nsign still reverses in {int(d.core_sign_flips.sum())}/{len(d)} channels on the core set")
print(f"median core spread {d.core_spread.median():.0f} d "
      f"vs full {d.full_spread.median():.0f} d")
d.to_csv("paper3_core_subset.csv", index=False)

# ------------------------------------------------- (2) operational consequence
from paper3_common import SEASONS, load_flux
import itertools

df_raw = load_flux()
STAT = ["sd1.645", "sd1.96", "sd2.58", "p90", "p95", "p97.5"]
NONSEASON = [0.25, 0.40, 0.50]
COVID = ["exclude_2020_2022", "exclude_2020", "include_all"]
SMOOTH = [False, True]
SUSTAIN = [1, 2]


def covid_mask(d, mode):
    if mode == "exclude_2020_2022":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2022-12-31"))
    if mode == "exclude_2020":
        return ~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2020-12-31"))
    return pd.Series(True, index=d.index)


def threshold(v, stat):
    v = pd.Series(v).dropna()
    if len(v) < 5:
        return np.inf
    return (v.mean() + float(stat[2:]) * v.std()) if stat.startswith("sd") \
        else v.quantile(float(stat[1:]) / 100)


def first_cross(series, dates, thr, sustain):
    above = (series > thr).values
    for i in range(len(above) - sustain + 1):
        if above[i:i + sustain].all():
            return dates.iloc[i]
    return None


FOCUS = "Adm_0_5"   # the channel most often proposed as a paediatric sentinel
out = []
for name, start, end in SEASONS:
    dates_found = []
    for stat, nsq, cov, sm, sus in itertools.product(STAT, NONSEASON, COVID, SMOOTH, SUSTAIN):
        if (cov == "include_all") + (nsq == 0.25) + (stat == "p90") > 2:
            continue                       # core set only
        d = df_raw.copy()
        if sm:
            d[FOCUS] = d[FOCUS].rolling(3, center=True, min_periods=1).mean()
        pool = d[covid_mask(d, cov)].dropna(subset=["AandB_proportion"])
        ns = pool[pool.AandB_proportion < pool.AandB_proportion.quantile(nsq)]
        thr = threshold(ns[FOCUS], stat)
        s = d[(d.MidDate >= start) & (d.MidDate <= end)].dropna(subset=[FOCUS])
        if len(s) < 8:
            continue
        cd = first_cross(s[FOCUS], s.MidDate, thr, sus)
        if cd is not None:
            dates_found.append(cd)
    if dates_found:
        lo, hi = min(dates_found), max(dates_found)
        out.append({"season": name, "earliest_declaration": lo.date(),
                    "latest_declaration": hi.date(),
                    "gap_days": (hi - lo).days,
                    "gap_weeks": round((hi - lo).days / 7, 1),
                    "n_specs": len(dates_found)})

ops = pd.DataFrame(out)
print("\n=== OPERATIONAL CONSEQUENCE: when would 0-5y admissions declare onset? ===")
print("(core specifications only; each row is one season)")
print(ops.to_string(index=False))
print(f"\nmedian gap between earliest and latest defensible declaration: "
      f"{ops.gap_weeks.median():.1f} weeks; maximum {ops.gap_weeks.max():.1f} weeks")
ops.to_csv("paper3_operational_gap.csv", index=False)
