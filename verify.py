"""
Check every headline number in the manuscript against the regenerated results.

Run by runall.sh as its last step, so a value that drifts breaks the build
rather than reaching a draft. Exits nonzero on any failure.

Part II rule: "the check is not 'did I update the manuscript' but 'do all four
still agree'."
"""

import os
import re
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figures")
MS = os.path.join(ROOT, "manuscript", "paper3_manuscript.md")

FAILURES = []
CHECKS = 0


def check(condition, label, got=""):
    global CHECKS
    CHECKS += 1
    if condition:
        print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}   {got}")
        FAILURES.append(label)


def band(d):
    for b in ["201-400", "101-200", "51-100", "21-50"]:
        if b in d.subtree_size.unique():
            return d[d.subtree_size == b]
    return d


thr = pd.read_csv(os.path.join(RES, "paper3_anchor_speccurve.csv"))
rt = pd.read_csv(os.path.join(RES, "paper3_rt_speccurve.csv"))
mem = pd.read_csv(os.path.join(RES, "paper3_mem_speccurve.csv"))
com = pd.read_csv(os.path.join(RES, "paper3_common_subspace.csv"))
text = open(MS).read()

print("\n--- specification space ---")
check(len(thr) == 22464, "22,464 threshold estimates", f"got {len(thr)}")
check(thr.spec_id.nunique() == 1728, "1,728 threshold specifications",
      f"got {thr.spec_id.nunique()}")
check(rt.spec_id.nunique() == 864, "864 R(t) specifications",
      f"got {rt.spec_id.nunique()}")
check(mem.spec_id.nunique() == 576, "576 MEM specifications",
      f"got {mem.spec_id.nunique()}")
check(com.spec_id.nunique() == 48, "48 shared specifications",
      f"got {com.spec_id.nunique()}")

print("\n--- dimension swings (Table 2) ---")
cc = thr[thr.median_lead.notna()]
sw = {d: round(float(cc.groupby(d).median_lead.mean().max()
                     - cc.groupby(d).median_lead.mean().min()), 1)
      for d in ["anchor", "comparator", "stat", "nonseason_q",
                "seasonset", "covid", "sustain", "smooth"]}
for dim, expect in [("anchor", 26.3), ("comparator", 18.9), ("stat", 12.2),
                    ("nonseason_q", 9.8), ("seasonset", 7.3), ("covid", 7.1),
                    ("sustain", 3.2), ("smooth", 2.8)]:
    check(abs(sw[dim] - expect) < 0.05, f"swing {dim} = {expect} d",
          f"got {sw[dim]}")
check(sw["anchor"] == max(sw.values()), "anchoring is the largest dimension")

print("\n--- anchoring effect ---")
mm = cc.groupby("anchor").median_lead.mean()
check(abs(mm["reference_series"] - (-14.7)) < 0.05,
      "reference anchoring mean -14.7 d", f"got {mm['reference_series']:.1f}")
check(abs(mm["own_series"] - 11.6) < 0.05,
      "own-series anchoring mean +11.6 d", f"got {mm['own_series']:.1f}")

print("\n--- dispersion ---")
flips = int(thr.groupby("channel").median_lead
            .agg(lambda v: (v > 0).any() and (v < 0).any()).sum())
check(flips == 13, "sign reverses in all 13 channels", f"got {flips}")
sp = thr.groupby("channel").median_lead.agg(lambda v: v.max() - v.min())
check(sp.min() == 105 and sp.max() == 217, "spreads span 105 to 217 d",
      f"got {sp.min()}-{sp.max()}")
pos = thr.dropna(subset=["median_lead"]).groupby("channel").median_lead \
         .agg(lambda v: 100 * (v > 0).mean())
check(round(pos.min()) == 14 and round(pos.max()) == 37,
      "positive lead in 14% to 37% of specifications",
      f"got {pos.min():.1f}-{pos.max():.1f}")

print("\n--- reference-anchored half reproduces the original analysis ---")
r = thr[thr.anchor == "reference_series"]
fr = int(r.groupby("channel").median_lead
         .agg(lambda v: (v > 0).any() and (v < 0).any()).sum())
sr = r.groupby("channel").median_lead.agg(lambda v: v.max() - v.min())
pr = r.dropna(subset=["median_lead"]).groupby("channel").median_lead \
      .agg(lambda v: 100 * (v > 0).mean())
check(fr == 12, "12 of 13 channels reverse sign", f"got {fr}")
check(sr.min() == 105 and sr.max() == 189, "spreads 105 to 189 d",
      f"got {sr.min()}-{sr.max()}")
check(round(pr.min(), 1) == 0.0 and round(pr.max(), 1) == 20.6,
      "positive lead 0% to 20.6%", f"got {pr.min():.1f}-{pr.max():.1f}")

print("\n--- equal-terms comparison (Table 2b) ---")
res = {}
for fam in ("threshold", "mem", "rt"):
    g = com[com.family == fam]
    s = g.groupby("channel").median_lead.agg(
        lambda v: (v.max() - v.min()) if v.notna().any() else np.nan)
    f = int(g.groupby("channel").median_lead
            .agg(lambda v: bool((v > 0).any() and (v < 0).any())).sum())
    res[fam] = (round(s.median(), 1), round(s.min(), 1), round(s.max(), 1), f)
check(res["threshold"][:3] == (35.0, 21.0, 101.5),
      "threshold 35.0 d (21.0-101.5)", f"got {res['threshold'][:3]}")
check(res["mem"][:3] == (49.0, 31.5, 91.0), "MEM 49.0 d (31.5-91.0)",
      f"got {res['mem'][:3]}")
check(res["rt"][:3] == (77.0, 56.0, 140.0), "R(t) 77.0 d (56.0-140.0)",
      f"got {res['rt'][:3]}")
check(res["threshold"][3] == 7, "threshold reverses in 7 of 13",
      f"got {res['threshold'][3]}")
check(res["mem"][3] == 0, "MEM reverses in 0 of 13", f"got {res['mem'][3]}")
check(res["rt"][3] == 13, "R(t) reverses in 13 of 13", f"got {res['rt'][3]}")
check(res["threshold"][0] < res["mem"][0],
      "ordering reverses: threshold narrower than MEM on equal terms")

print("\n--- full-space family behaviour (Table 3) ---")
mf = int(mem.groupby("channel").median_lead
         .agg(lambda v: (v > 0).any() and (v < 0).any()).sum())
check(mf == 1, "MEM reverses in 1 of 13 on its own space", f"got {mf}")
rp = rt.dropna(subset=["median_lead"]).groupby("channel").median_lead \
       .agg(lambda v: 100 * (v > 0).mean())
check(round(rp.min()) == 73 and round(rp.max()) == 100,
      "R(t) leads in 73% to 100%", f"got {rp.min():.1f}-{rp.max():.1f}")
ms = mem.groupby("channel").median_lead.agg(lambda v: v.max() - v.min())
check(abs(ms.median() - 45.5) < 0.6, "MEM median spread 45.5 d",
      f"got {ms.median()}")

print("\n--- manuscript limits ---")
body = text.split("# Introduction", 1)[1].split("# Tables", 1)[0]
words = len(re.sub(r"\[[0-9,\-–]+\]", "", body).split())
abstract = len(text.split("# Abstract", 1)[1].split("# Introduction", 1)[0].split())
check(words <= 3500, f"body {words} words (limit 3,500)")
check(abstract <= 250, f"abstract {abstract} words (limit 250)")
refs = [l for l in text.split("# References")[1].splitlines()
        if re.match(r"^\d+\.", l.strip())]
cited = set()
for m in re.findall(r"\[([0-9,\-–\s]+)\]", text.split("# References")[0]):
    for p in m.split(","):
        p = p.strip()
        if p.isdigit():
            cited.add(int(p))
check(len(refs) == 18, f"18 references ({len(refs)})")
check(not [i for i in range(1, len(refs) + 1) if i not in cited],
      "every reference is cited")
check(text.count("![") == 4, f"4 illustrations ({text.count('![')})")

print("\n--- figures on disk ---")
for f in ["paper3_fig1_speccurve.png", "paper3_fig3_allchannels.png",
          "paper3_fig4_method_families.png", "paper3_fig2_allages.png"]:
    p = os.path.join(FIG, f)
    check(os.path.exists(p) and os.path.getsize(p) > 20000, f"{f} present")

print("\n--- no stale genomic content ---")
check(not re.search(r"\b(genom|clade|lineage|GISAID|phylo)", text, re.I),
      "manuscript contains no genomic claims")

print(f"\n{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
if FAILURES:
    print("FAILED:")
    for f in FAILURES:
        print("  -", f)
    sys.exit(1)
print("All manuscript numbers agree with regenerated results.")
