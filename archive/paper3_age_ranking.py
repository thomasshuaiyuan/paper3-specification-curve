"""
Paper 3 groundwork: settle which age group signals influenza onset earliest,
and how much that answer depends on the definition.

v7 reports the 12-17y group crossing its baseline first in 3 of 5 seasons.
A quick baseline-crossing pass gave 0-5y first in 6 of 8. Before either number
goes in a paper, establish how sensitive the ranking is to the choices that
were made silently:

  - baseline multiplier         (1.645 / 1.96 / 2.58 SD above non-season mean)
  - non-season definition       (positivity below median / below 25th pct)
  - COVID-era exclusion         (2020-2022 dropped or kept in the baseline pool)
  - season set                  (5 single-wave vs all 8 admissions-eligible)
  - ranking target              (earliest among groups vs earliest vs CHP threshold)

If the ranking flips across these, the age-group claim is not robust and v7's
version needs softening. If it holds, Paper 3 has a finding and v7 has support.
No neural network anywhere in this.
"""

import itertools

import numpy as np
import pandas as pd

from seir_pinn_multisignal import CHP_THRESHOLD, SEASONS, load_flux

AGE = ["Adm_0_5", "Adm_6_11", "Adm_12_17", "Adm_18_49", "Adm_50_64", "Adm_65_higher"]
SINGLE_WAVE = ["2014/15 winter", "2015/16 winter", "2018/19 winter",
               "2023 summer", "2024/25 winter"]

df = load_flux()
pd.set_option("display.width", 240, "display.max_columns", 40)


def baselines(mult, nonseason_q, drop_covid):
    d = df
    if drop_covid:
        d = d[~((d.MidDate >= "2020-01-01") & (d.MidDate <= "2022-12-31"))]
    d = d.dropna(subset=["AandB_proportion"])
    cut = d.AandB_proportion.quantile(nonseason_q)
    ns = d[d.AandB_proportion < cut]
    return {a: ns[a].mean() + mult * ns[a].std() for a in AGE}


def rank_for(spec, season_set):
    base = baselines(*spec)
    first_counts, leads = {a: 0 for a in AGE}, {a: [] for a in AGE}
    for name, start, end in SEASONS:
        if name not in season_set:
            continue
        s = df[(df.MidDate >= start) & (df.MidDate <= end)].dropna(subset=["AandB_proportion"])
        chp = s[s.AandB_proportion > CHP_THRESHOLD]
        chp_date = chp.iloc[0].MidDate if len(chp) else None
        cross = {}
        for a in AGE:
            c = s[s[a] > base[a]]
            if len(c):
                cross[a] = c.iloc[0].MidDate
                if chp_date is not None:
                    leads[a].append((chp_date - c.iloc[0].MidDate).days)
        if cross:
            first_counts[min(cross, key=cross.get)] += 1
    return first_counts, {a: (np.median(v) if v else np.nan) for a, v in leads.items()}


print("=" * 78)
print("SENSITIVITY OF THE AGE-GROUP RANKING")
print("=" * 78)
rows = []
for mult, q, drop, sset_name in itertools.product(
        [1.645, 1.96, 2.58], [0.5, 0.25], [True, False],
        ["all8", "single5"]):
    sset = SINGLE_WAVE if sset_name == "single5" else [s[0] for s in SEASONS]
    counts, med_leads = rank_for((mult, q, drop), sset)
    winner = max(counts, key=counts.get)
    rows.append({"mult": mult, "nonseason_q": q, "drop_covid": drop, "seasons": sset_name,
                 "earliest_group": winner, "n_seasons_won": counts[winner],
                 "12_17_wins": counts["Adm_12_17"], "0_5_wins": counts["Adm_0_5"],
                 "median_lead_12_17": med_leads["Adm_12_17"],
                 "median_lead_0_5": med_leads["Adm_0_5"]})

res = pd.DataFrame(rows)
res.to_csv("paper3_age_sensitivity.csv", index=False)
print(res.to_string(index=False))

print("\n" + "=" * 78)
print("HOW OFTEN DOES EACH GROUP WIN, ACROSS ALL 24 SPECIFICATIONS?")
print("=" * 78)
print(res.earliest_group.value_counts().to_string())
print(f"\n12-17y is the earliest group in {int((res.earliest_group=='Adm_12_17').sum())}/{len(res)} specifications")
print(f"0-5y   is the earliest group in {int((res.earliest_group=='Adm_0_5').sum())}/{len(res)} specifications")
print(f"\n12-17y median lead range across specs: "
      f"{res.median_lead_12_17.min():.0f} to {res.median_lead_12_17.max():.0f} days")
print(f"0-5y   median lead range across specs: "
      f"{res.median_lead_0_5.min():.0f} to {res.median_lead_0_5.max():.0f} days")
