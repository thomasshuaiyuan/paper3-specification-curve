#!/usr/bin/env python3
"""
One-panel summary of the specification analysis, Hong Kong beside the United States.

Shows, for every surveillance channel in both systems, the full range of median
onset lead across all defensible threshold-crossing specifications. The point is
that the range crosses zero in every channel of both systems: whether a signal
appears to lead or lag laboratory positivity has no specification-independent
answer.

Place in src/figures/. Run from the repository root:

    python src/figures/paper3_fig_hk_us.py

Writes figures/paper3_fig_hk_us.png. Exits nonzero if an input is missing or a
column cannot be resolved, rather than producing a partial figure.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------------------------- paths
ROOT = Path(__file__).resolve().parents[2]
HK_CURVE = ROOT / "results" / "paper3_anchor_speccurve.csv"
US_CURVE = ROOT / "us" / "fluview_speccurve.csv"
OUT = ROOT / "figures" / "paper3_fig_hk_us.png"

# ------------------------------------------------------------ column mapping
# HK columns are known from paper3_anchor_speccurve.py. The US writer was run
# separately; if it named its columns differently, set US_CHANNEL / US_LEAD
# here rather than editing the body.
HK_CHANNEL, HK_LEAD = "channel", "median_lead"
US_CHANNEL, US_LEAD = "channel", "median_lead"

# Hong Kong labels, matching src/paper3_common.py.
HK_LABEL = {
    "ILI_PMP": "Outpatient (private GP)",
    "ILI_AED": "Emergency attendance",
    "ILI_CMP": "Traditional medicine",
    "ILI_School": "School outbreaks",
    "ILI_NonSchool": "Non-school outbreaks",
    "Fever_RCHE": "Care-home fever",
    "Adm_All": "Admissions, all ages",
    "Adm_0_5": "Admissions 0-5y",
    "Adm_6_11": "Admissions 6-11y",
    "Adm_12_17": "Admissions 12-17y",
    "Adm_18_49": "Admissions 18-49y",
    "Adm_50_64": "Admissions 50-64y",
    "Adm_65_higher": "Admissions 65+y",
}

# FluSurv-NET / ILINet labels.
US_LABEL = {
    "rate_age_0tlt1": "Hospitalisations <1y",
    "rate_age_1t4": "Hospitalisations 1-4y",
    "rate_age_5t11": "Hospitalisations 5-11y",
    "rate_age_12t17": "Hospitalisations 12-17y",
    "rate_age_18t29": "Hospitalisations 18-29y",
    "rate_age_30t39": "Hospitalisations 30-39y",
    "rate_age_40t49": "Hospitalisations 40-49y",
    "rate_age_gte75": "Hospitalisations 75+y",
    "rate_overall": "Hospitalisations, all ages",
    "wili": "ILINet weighted ILI",
}

SIGNAL_FIRST = "#2c6fad"      # signal crosses before positivity
POSITIVITY_FIRST = "#d1741f"  # positivity crosses first
SPAN = "#8a8a8a"


def load(path, channel_col, lead_col, labels, system):
    """Collapse a specification curve to one min/median/max row per channel."""
    if not path.exists():
        sys.exit(f"missing input: {path}")
    df = pd.read_csv(path)
    for col in (channel_col, lead_col):
        if col not in df.columns:
            sys.exit(
                f"{path.name}: no column '{col}'. Present: {list(df.columns)}. "
                "Set the mapping constants at the top of this script."
            )
    df = df[df[lead_col].notna()]
    if df.empty:
        sys.exit(f"{path.name}: no non-null values in '{lead_col}'")

    out = (
        df.groupby(channel_col)[lead_col]
        .agg(lo="min", mid="median", hi="max")
        .reset_index()
        .rename(columns={channel_col: "channel"})
    )
    unlabelled = set(out.channel) - set(labels)
    if unlabelled:
        sys.exit(f"{path.name}: unlabelled channels {sorted(unlabelled)}")
    out["label"] = out.channel.map(labels)
    out["system"] = system
    return out.sort_values("mid").reset_index(drop=True)


def draw(ax, d, title):
    """One row per channel. Each range is split at zero so that a bar carrying
    both colours is, by eye, a channel whose answer reverses."""
    y = list(range(len(d)))
    ax.axvline(0, color="black", lw=1.4, zorder=5)

    # left of zero: positivity crosses first. Right of zero: the signal does.
    ax.hlines(y, d.lo.clip(upper=0), 0, color=POSITIVITY_FIRST, lw=6, zorder=2)
    ax.hlines(y, 0, d.hi.clip(lower=0), color=SIGNAL_FIRST, lw=6, zorder=2)
    ax.scatter(d.mid, y, s=46, color="white", edgecolor="black",
               linewidth=1.2, zorder=6)

    reversing = int(((d.lo < 0) & (d.hi > 0)).sum())
    ax.set_yticks(y)
    ax.set_yticklabels(d.label)
    ax.set_title(title, loc="left", fontsize=11.5, fontweight="bold", pad=10)
    ax.set_xlabel("Median lead against laboratory positivity (days)", labelpad=8)
    ax.margins(y=0.05)
    ax.grid(axis="x", color="#e2e2e2", lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.annotate(
        f"Range spans zero in {reversing} of {len(d)} channels",
        xy=(0.5, -0.155), xycoords="axes fraction", ha="center",
        fontsize=10, fontweight="bold", color="#333333",
    )


def main():
    hk = load(HK_CURVE, HK_CHANNEL, HK_LEAD, HK_LABEL, "hk")
    us = load(US_CURVE, US_CHANNEL, US_LEAD, US_LABEL, "us")

    fig, axes = plt.subplots(
        1, 2, figsize=(13.5, 5.6), sharex=True,
        gridspec_kw={"width_ratios": [len(hk), len(us)], "wspace": 0.55},
    )
    draw(axes[0], hk, f"Hong Kong, 2014-2026 ({len(hk)} channels)")
    draw(axes[1], us, f"United States, 2016/17-2025/26 ({len(us)} channels)")

    handles = [
        plt.Line2D([], [], color=POSITIVITY_FIRST, lw=6,
                   label="Specifications under which laboratory positivity crosses first"),
        plt.Line2D([], [], color=SIGNAL_FIRST, lw=6,
                   label="Specifications under which the signal crosses first"),
        plt.Line2D([], [], marker="o", ls="", color="white", markersize=8,
                   markeredgecolor="black", label="Median across all specifications"),
    ]
    fig.legend(
        handles=handles, loc="lower center", ncol=3, frameon=False,
        bbox_to_anchor=(0.5, -0.085), fontsize=9.5,
    )
    fig.suptitle(
        "The sign of the onset lead reverses in every channel of both systems",
        x=0.008, ha="left", fontsize=13, fontweight="bold", y=1.0,
    )
    fig.text(
        0.008, 0.945,
        "Range of median lead across all defensible threshold-crossing "
        "specifications. Left of zero, laboratory positivity crosses first; "
        "right of zero, the signal does.",
        ha="left", fontsize=9.5, color="#444444",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_name(OUT.name + ".partial")
    fig.savefig(tmp, dpi=300, format="png", bbox_inches="tight", facecolor="white")
    tmp.rename(OUT)
    plt.close(fig)

    for d, name in ((hk, "Hong Kong"), (us, "United States")):
        reversing = int(((d.lo < 0) & (d.hi > 0)).sum())
        print(
            f"{name}: sign reverses in {reversing}/{len(d)} channels; "
            f"spreads {(d.hi - d.lo).min():.0f} to {(d.hi - d.lo).max():.0f} days"
        )
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
