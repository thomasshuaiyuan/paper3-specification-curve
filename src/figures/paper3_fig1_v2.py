"""Paper 3 Figure 1 — specification curve, in the standard two-panel form."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SURFACE, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE = "#2a78d6", "#eb6834"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"],
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": BASE,
    "axes.labelcolor": INK2, "text.color": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

curve = pd.read_csv("paper3_anchor_speccurve.csv")
AGE_LABEL = {"Adm_0_5": "0–5y", "Adm_6_11": "6–11y", "Adm_12_17": "12–17y",
             "Adm_18_49": "18–49y", "Adm_50_64": "50–64y", "Adm_65_higher": "65+y"}
FOCUS = "ILI_PMP"

DIMS = [("anchor", "Baseline anchoring"), ("comparator", "Comparator threshold"),
        ("covid", "Pandemic-era handling"),
        ("nonseason_q", "Non-season definition"), ("stat", "Baseline statistic"),
        ("seasonset", "Season set"), ("sustain", "Sustained-crossing rule"),
        ("smooth", "Smoothing")]

sub = curve[(curve.channel == FOCUS) & curve.median_lead.notna()].copy()
sub = sub.sort_values("median_lead").reset_index(drop=True)
sub["x"] = np.arange(len(sub))

fig = plt.figure(figsize=(13, 9))
gs = fig.add_gridspec(2, 1, height_ratios=[1.5, 2.0], hspace=0.06)

# ---- top: the curve --------------------------------------------------------
ax = fig.add_subplot(gs[0])
cols = np.where(sub.median_lead > 0, BLUE, ORANGE)
ax.bar(sub.x, sub.median_lead, width=1.0, color=cols, linewidth=0)
ax.axhline(0, color=INK2, lw=1.2)
ax.set_ylabel("Median lead over the positivity\nthreshold (days)", fontsize=10)
ax.set_xlim(-4, len(sub) + 3)
ax.set_xticks([])
ax.set_title("Onset lead time for private outpatient consultations, "
             f"under all {len(sub)} defensible specifications",
             fontsize=13, color=INK, loc="left", pad=12)
pos = 100 * (sub.median_lead > 0).mean()
ax.text(0.015, 0.93,
        f"The signal crosses first (positive lead) in {pos:.0f}% of specifications.\n"
        f"Range {sub.median_lead.min():.0f} to {sub.median_lead.max():.0f} days on identical data.",
        transform=ax.transAxes, fontsize=10, color=INK2, va="top")

# ---- bottom: which choice produced each specification ----------------------
ax2 = fig.add_subplot(gs[1], sharex=ax)
ypos, ylabels, yticks = 0, [], []
for dim, label in DIMS:
    levels = sorted(sub[dim].astype(str).unique())
    for lev in levels:
        m = (sub[dim].astype(str) == lev).values
        ax2.scatter(sub.x[m], np.full(m.sum(), ypos), s=1.6,
                    color=INK2, marker="s", linewidths=0)
        yticks.append(ypos)
        ylabels.append(f"{label}  —  {lev}" if lev == levels[0] else f"{lev}")
        ypos -= 1
    ypos -= 0.6

ax2.set_yticks(yticks)
ax2.set_yticklabels(ylabels, fontsize=8.2, color=INK2)
ax2.set_xlabel("Specifications, ordered by the lead time they produce", fontsize=10)
ax2.set_ylim(ypos, 1)
ax2.set_xlim(-4, len(sub) + 3)
ax2.tick_params(axis="x", labelsize=9)

fig.text(0.008, 0.008,
         "Each column is one analysis of the same Hong Kong CHP data, 2014–2026. "
         "Blue = the signal crosses before laboratory positivity; orange = after. "
         "Seven analytic choices fully crossed; none is routinely reported.",
         fontsize=8.4, color=MUTED)
fig.subplots_adjust(left=0.235, right=0.985, top=0.93, bottom=0.075)
fig.savefig("paper3_fig1_speccurve.png", dpi=200, facecolor=SURFACE)
print("wrote paper3_fig1_speccurve.png")

