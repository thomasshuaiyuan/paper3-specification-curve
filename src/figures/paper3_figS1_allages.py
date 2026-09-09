"""
Supplementary Figure S1 — specification curves for the six age-stratified
admission series, on the full 1,728-specification space.

Replaces the earlier paper3_figure.py, which read the superseded 864-row
paper3_speccurve.csv and, as a side effect, overwrote the in-text Figure 1 with
a stale version. This script writes one file and only one file.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SURFACE, INK, INK2, MUTED, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#c3c2b7"
BLUE, ORANGE = "#2a78d6", "#eb6834"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

AGE_LABEL = {"Adm_0_5": "0–5y", "Adm_6_11": "6–11y", "Adm_12_17": "12–17y",
             "Adm_18_49": "18–49y", "Adm_50_64": "50–64y",
             "Adm_65_higher": "65+y"}

curve = pd.read_csv("paper3_anchor_speccurve.csv")
# Read off the curve so the caption cannot drift from the data.
NSPEC = curve.spec_id.nunique()

fig, axes = plt.subplots(2, 3, figsize=(13.5, 6), sharey=True)
for ax, ch in zip(axes.ravel(), AGE_LABEL):
    s = (curve[(curve.channel == ch) & curve.median_lead.notna()]
         .sort_values("median_lead"))
    x = np.arange(len(s))
    ax.bar(x, s.median_lead, width=1.0,
           color=np.where(s.median_lead > 0, BLUE, ORANGE), linewidth=0)
    ax.axhline(0, color=INK2, lw=1.0)
    ax.set_title(f"{AGE_LABEL[ch]}  ({100*(s.median_lead>0).mean():.0f}% positive)",
                 fontsize=10.5, color=INK, loc="left")
    ax.set_xticks([])
for ax in axes[:, 0]:
    ax.set_ylabel("Median lead (days)", fontsize=9.5)

fig.suptitle("The sign of the lead reverses for every age group",
             fontsize=12.5, color=INK, x=0.008, ha="left", y=0.99)
fig.text(0.008, 0.005,
         f"Each panel sorts the {NSPEC:,} threshold-crossing specifications for that "
         "age group. Blue: admissions cross first. Orange: laboratory positivity "
         "crosses first.",
         fontsize=8.3, color=MUTED)
fig.tight_layout(rect=[0, 0.03, 1, 0.96])
fig.savefig("paper3_fig2_allages.png", dpi=200, facecolor=SURFACE)
print("wrote paper3_fig2_allages.png")
