"""Figure 3 — range of median lead time across 864 specifications, all 13 channels."""

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
    "axes.spines.top": False, "axes.spines.right": False,
})

LABEL = {
    "ILI_PMP": "Outpatient (private GP)", "ILI_AED": "Emergency attendance",
    "ILI_CMP": "Traditional medicine", "ILI_School": "School outbreaks",
    "ILI_NonSchool": "Non-school outbreaks", "Fever_RCHE": "Care-home fever",
    "Adm_All": "Admissions, all ages", "Adm_0_5": "Admissions 0–5y",
    "Adm_6_11": "Admissions 6–11y", "Adm_12_17": "Admissions 12–17y",
    "Adm_18_49": "Admissions 18–49y", "Adm_50_64": "Admissions 50–64y",
    "Adm_65_higher": "Admissions 65+y",
}
ORDER = ["ILI_PMP", "ILI_AED", "ILI_CMP", "ILI_School", "ILI_NonSchool", "Fever_RCHE",
         "Adm_All", "Adm_0_5", "Adm_6_11", "Adm_12_17", "Adm_18_49", "Adm_50_64", "Adm_65_higher"]
GROUPS = [("Outpatient", ["ILI_PMP"]), ("Emergency", ["ILI_AED"]),
          ("Traditional medicine", ["ILI_CMP"]),
          ("Institutional outbreak", ["ILI_School", "ILI_NonSchool"]),
          ("Care-home fever", ["Fever_RCHE"]),
          ("Hospital admissions", ["Adm_All", "Adm_0_5", "Adm_6_11", "Adm_12_17",
                                   "Adm_18_49", "Adm_50_64", "Adm_65_higher"])]

c = pd.read_csv("paper3_anchor_speccurve.csv")
fig, ax = plt.subplots(figsize=(11, 7))

y, yticks, ylabels, seps = 0, [], [], []
for gname, chans in GROUPS:
    for ch in chans:
        s = c[c.channel == ch].median_lead.dropna()
        lo, hi, med = s.min(), s.max(), s.median()
        pos = 100 * (s > 0).mean()
        ax.plot([lo, hi], [y, y], color=BASE, lw=6, solid_capstyle="round", zorder=1)
        neg_hi = min(hi, 0)
        if lo < 0:
            ax.plot([lo, neg_hi], [y, y], color=ORANGE, lw=6, solid_capstyle="round", zorder=2)
        if hi > 0:
            ax.plot([max(lo, 0), hi], [y, y], color=BLUE, lw=6, solid_capstyle="round", zorder=2)
        ax.scatter([med], [y], s=46, color=INK, zorder=4,
                   edgecolor=SURFACE, linewidth=1.5)
        ax.text(hi + 5, y, f"{pos:.0f}% positive", fontsize=8.4, color=MUTED, va="center")
        yticks.append(y); ylabels.append(LABEL[ch]); y -= 1
    seps.append(y + 0.5); y -= 0.7

ax.axvline(0, color=INK2, lw=1.2, zorder=3)
for s_ in seps[:-1]:
    ax.axhline(s_, color=GRID, lw=0.9, zorder=0)
ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=9.6, color=INK2)
ax.set_ylim(y + 0.4, 0.8)
ax.set_xlim(-140, 128)
ax.set_xlabel("Median lead over the laboratory positivity threshold (days), "
              "across 864 specifications", fontsize=10)
ax.set_title("The sign of the lead reverses in every surveillance channel",
             fontsize=13, color=INK, loc="left", pad=12)

handles = [plt.Line2D([], [], color=BLUE, lw=6), plt.Line2D([], [], color=ORANGE, lw=6),
           plt.Line2D([], [], color=INK, marker="o", lw=0, markersize=7)]
ax.legend(handles, ["Signal crosses first", "Positivity crosses first", "Median across specifications"],
          frameon=False, fontsize=9, loc="upper center", ncol=3,
          bbox_to_anchor=(0.5, -0.10), labelcolor=INK2)
fig.text(0.008, 0.005,
         "Each bar spans the full range of median lead time obtainable from the same Hong Kong CHP data "
         "by varying eight analytic choices, of which baseline anchoring is the largest.",
         fontsize=8.3, color=MUTED)
fig.subplots_adjust(left=0.30, right=0.98, top=0.93, bottom=0.16)
fig.savefig("paper3_fig3_allchannels.png", dpi=200, facecolor=SURFACE)
print("wrote paper3_fig3_allchannels.png")
