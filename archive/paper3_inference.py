"""Permutation inference for the Paper 3 specification curve."""

import numpy as np
import pandas as pd

rng = np.random.default_rng(20260807)
AGE = ["Adm_0_5", "Adm_6_11", "Adm_12_17", "Adm_18_49", "Adm_50_64", "Adm_65_higher"]

dom = pd.read_csv("/root/paper2/paper3_dominance.csv")
curve = pd.read_csv("/root/paper2/paper3_speccurve.csv")

# ---- Test 1: is the dominance pattern stronger than chance? -----------------
# Null: within each specification-season, the earliest group is arbitrary.
obs_share = dom.earliest.value_counts(normalize=True)
obs_max = float(obs_share.max())
obs_winner = obs_share.idxmax()

n_perm = 2000
null_max = np.empty(n_perm)
n = len(dom)
for i in range(n_perm):
    draw = rng.integers(0, len(AGE), size=n)
    null_max[i] = np.bincount(draw, minlength=len(AGE)).max() / n

p_dom = float((null_max >= obs_max).mean())
print("=== TEST 1: dominance vs chance ===")
print(f"  observed: {obs_winner} earliest in {100*obs_max:.1f}% of {n} specification-seasons")
print(f"  chance baseline (6 groups): {100/len(AGE):.1f}%")
print(f"  null max-share distribution: mean {100*null_max.mean():.1f}%, "
      f"97.5th pct {100*np.quantile(null_max, .975):.1f}%")
print(f"  p = {p_dom:.4f}" + ("  (< 1/2000)" if p_dom == 0 else ""))

# ---- Test 2: is 12-17y's near-absence stronger than chance? ----------------
obs_1217 = float(obs_share.get("Adm_12_17", 0.0))
null_1217 = np.array([np.bincount(rng.integers(0, len(AGE), size=n),
                                  minlength=len(AGE))[2] / n for _ in range(n_perm)])
p_1217 = float((null_1217 <= obs_1217).mean())
print("\n=== TEST 2: 12-17y earliest less often than chance? ===")
print(f"  observed: {100*obs_1217:.1f}%   chance: {100/len(AGE):.1f}%   p = {p_1217:.4f}")

# ---- Test 3: direction of the lead ----------------------------------------
print("\n=== TEST 3: how often does any specification give a POSITIVE lead? ===")
for a in AGE:
    v = curve[(curve.age == a)].median_lead.dropna()
    pos = float((v > 0).mean())
    lo, hi = np.quantile(v, [.025, .975])
    print(f"  {a:<16} positive in {100*pos:>5.1f}% of specs | "
          f"median {np.median(v):>6.1f} d | 95% span {lo:>6.1f} to {hi:>5.1f} d")

# ---- Test 4: which single choice would a reader most need to know? ---------
print("\n=== TEST 4: swing attributable to each choice (max - min of group means) ===")
rows = []
for a in AGE:
    sub = curve[(curve.age == a) & curve.median_lead.notna()]
    for dim in ["stat", "nonseason_q", "covid", "smooth", "sustain", "seasonset", "comparator"]:
        m = sub.groupby(dim).median_lead.mean()
        rows.append({"age": a, "choice": dim, "swing_days": round(float(m.max() - m.min()), 1)})
sw = pd.DataFrame(rows).pivot(index="choice", columns="age", values="swing_days")
sw["mean_swing"] = sw.mean(axis=1).round(1)
print(sw.sort_values("mean_swing", ascending=False).to_string())

pd.DataFrame({"test": ["dominance_p", "adolescent_p"], "value": [p_dom, p_1217]}).to_csv(
    "/root/paper2/paper3_inference.csv", index=False)
