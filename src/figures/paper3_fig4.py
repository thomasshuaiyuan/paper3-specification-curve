"""Figure: threshold-crossing vs R(t)-based onset, same channels, same data."""

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

thr = pd.read_csv("paper3_anchor_speccurve.csv")
rt = pd.read_csv("paper3_rt_speccurve.csv")
mem = pd.read_csv("paper3_mem_speccurve.csv")
AQUA = "#1baf7a"

fig, ax = plt.subplots(figsize=(12, 8.6))
for i, ch in enumerate(ORDER):
    y = -i
    for src, off, colour, name in [(thr, 0.26, ORANGE, "Threshold crossing"),
                                   (mem, 0.0, AQUA, "Moving epidemic method"),
                                   (rt, -0.26, BLUE, "R(t) > 1")]:
        s = src[src.channel == ch].median_lead.dropna()
        if s.empty:
            continue
        ax.plot([s.min(), s.max()], [y + off] * 2, color=colour, lw=4.4, alpha=0.8,
                solid_capstyle="round", zorder=2)
        ax.scatter([s.median()], [y + off], s=26, color=INK, zorder=4,
                   edgecolor=SURFACE, linewidth=1.2)
        ax.text(s.max() + 6, y + off, f"{100*(s>0).mean():.0f}%", fontsize=7.0,
                color=MUTED, va="center")

ax.axvline(0, color=INK2, lw=1.2, zorder=3)
ax.set_yticks([-i for i in range(len(ORDER))])
ax.set_yticklabels([LABEL[c] for c in ORDER], fontsize=9.6, color=INK2)
ax.set_ylim(-len(ORDER) + 0.4, 0.7)
ax.set_xlim(-330, 130)
ax.set_xlabel("Median lead over the laboratory positivity threshold (days), "
              "across 576-864 specifications per method", fontsize=10)
ax.set_title("Two of three method families agree on direction; only one never reverses",
             fontsize=13, color=INK, loc="left", pad=12)

handles = [plt.Line2D([], [], color=ORANGE, lw=5), plt.Line2D([], [], color=AQUA, lw=5),
           plt.Line2D([], [], color=BLUE, lw=5),
           plt.Line2D([], [], color=INK, marker="o", lw=0, markersize=6)]
ax.legend(handles, ["Threshold crossing", "Moving epidemic method", "R(t) > 1 (renewal equation)",
                    "Median across specifications"],
          frameon=False, fontsize=9, loc="upper center", ncol=4,
          bbox_to_anchor=(0.5, -0.10), labelcolor=INK2)
fig.text(0.008, 0.006,
         "Percentages give the share of specifications yielding a positive lead. "
         "R(t) > 1 marks the onset of growth; threshold and MEM criteria mark accumulated magnitude, "
         "so part of the gap is definitional.",
         fontsize=8.2, color=MUTED)
fig.subplots_adjust(left=0.215, right=0.98, top=0.93, bottom=0.155)
fig.savefig("paper3_fig4_method_families.png", dpi=200, facecolor=SURFACE)
print("wrote paper3_fig4_method_families.png")


print("\n=== three-family comparison ===")
rows=[]
for ch in ORDER:
    a=thr[thr.channel==ch].median_lead.dropna(); b=rt[rt.channel==ch].median_lead.dropna()
    m=mem[mem.channel==ch].median_lead.dropna()
    rows.append({"channel":LABEL[ch],
        "thr_med":a.median(),"thr_pos":round(100*(a>0).mean(),1),"thr_spread":a.max()-a.min(),
        "mem_med":m.median(),"mem_pos":round(100*(m>0).mean(),1),"mem_spread":m.max()-m.min(),
        "rt_med":b.median(),"rt_pos":round(100*(b>0).mean(),1),"rt_spread":b.max()-b.min()})
d=pd.DataFrame(rows); pd.set_option("display.width",250)
print(d.to_string(index=False))
print(f"\nmedian spread: threshold {d.thr_spread.median():.0f} d | MEM {d.mem_spread.median():.0f} d | R(t) {d.rt_spread.median():.0f} d")
