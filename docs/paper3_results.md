# Paper 3 — Results Against the Pre-Specified Plan

*7 August 2026. Analysis run exactly as specified in `paper3_analysis_plan.md`, with no deviations. 864 specifications × 6 age groups = 5,184 estimates, plus 5,616 specification-seasons for the dominance analysis.*

## Headline

**On identical Hong Kong CHP data, the median admissions-based onset lead time for the 12–17y group ranges from −84 to +63 days depending on analytic choices that are almost never reported. The sign flips for every one of the six age groups.**

## 1. Dispersion

| Age group | Median | IQR | Range | Spread | Positive lead in |
|---|---|---|---|---|---|
| 0–5y | 0 d | −7 to 0 | −21 to +84 | **105 d** | 14.7% of specs |
| 6–11y | −7 d | −17.5 to 0 | −49 to +84 | **133 d** | 15.9% |
| 12–17y | −14 d | −28 to −7 | −84 to +63 | **147 d** | 7.6% |
| 18–49y | −7 d | −17.5 to 0 | −56 to +77 | **133 d** | 14.6% |
| 50–64y | 0 d | −7 to 0 | −56 to +84 | **140 d** | 20.6% |
| 65+y | −3.5 d | −7 to 0 | −56 to +84 | **140 d** | 18.1% |

**P1 confirmed** — spread exceeds 60 days for every group, not just one.
**P2 confirmed** — every group produces both positive and negative median leads.

The second finding is the one that will surprise people: **admissions cross before laboratory positivity in only 7.6%–20.6% of specifications.** The premise that age-stratified admissions provide early warning is a minority result within the space of defensible analyses, not a robust one. Under most reasonable choices, admissions cross their own baseline *after* positivity crosses the operational threshold.

## 2. Which choice matters

Mean swing in median lead attributable to each dimension, averaged across age groups:

| Analytic choice | Mean swing | Typically reported? |
|---|---|---|
| **Comparator threshold** (CHP operational vs data-derived) | **15.3 d** | No |
| **Pandemic-era handling** (exclude 2020–22 / 2020 / nothing) | **14.7 d** | Rarely |
| **Non-season definition** (25th / 40th / 50th percentile) | **12.8 d** | Rarely |
| Baseline statistic (SD multiplier or percentile) | 11.8 d | Sometimes |
| Season set (8 vs 5) | 1.6 d | Yes |
| Sustained-crossing rule (1 vs 2 weeks) | 1.3 d | Sometimes |
| Smoothing (none vs 3-week) | 0.8 d | Sometimes |

**P3 confirmed, and then some.** The three largest drivers are all choices that go unreported, while the two most often stated — season set and smoothing — barely move anything. Variance decomposition agrees: comparator alone explains 14–25% of variance in median lead depending on age group; smoothing and the sustained-crossing rule explain under 1%.

The practical implication is blunt: **a paper reporting an admissions-based lead time without stating its comparator threshold and its pandemic-era handling has not reported enough for the number to be interpretable.**

## 3. Dominance — which group is earliest

Across 5,616 specification-seasons:

| Age group | Earliest in |
|---|---|
| **0–5y** | **64.3%** |
| 50–64y | 15.6% |
| 65+y | 13.9% |
| 18–49y | 3.0% |
| 6–11y | 2.7% |
| **12–17y** | **0.5%** |

**P4 confirmed** — no group wins under all specifications. The exploratory 24-specification pass that gave 0–5y in 24 of 24 was itself an artifact of a too-small specification space, which is a tidy illustration of the paper's own thesis and should be reported as such.

Permutation inference (2,000 draws, uniform-random earliest group):

- 0–5y earliest in 64.3% against a chance baseline of 16.7%; null max-share distribution has mean 17.4% and 97.5th percentile 17.9%. **p < 0.0005.**
- 12–17y earliest in 0.5% against 16.7% chance. **p < 0.0005.**

So the ordering is not arbitrary — 0–5y genuinely leads more often than chance and 12–17y genuinely leads less — but neither result is specification-independent, and the *magnitude* of any lead is not stable at all.

## 4. What this says about the adolescent-admissions claim

12–17y is earliest in 0.5% of specification-seasons and has the most negative median lead of any group (−14 d). This is relevant to v7, where adolescent admissions are one of three headline claims — but the two analyses are not the same test. v7 reports EpiEstim-based leads and a Table S1 baseline-crossing count over 5 seasons; this is threshold-crossing over 864 specifications and 8 seasons. **The honest statement is that the adolescent finding does not appear robust to specification, not that it is wrong.** Thomas has indicated my earlier reading of v7 on this point was mistaken, and that correction has not yet been folded in here — it should be before anything is drafted.

## 5. Figures

- **Figure 1** (`paper3_fig1_speccurve.png`) — the specification curve for 12–17y: 864 sorted estimates above, the seven analytic choices below, so a reader sees which decisions push the estimate across zero.
- **Figure 2** (`paper3_fig2_allages.png`) — the same curve for all six age groups, compact, showing the sign flip is universal.

## 6. Scored predictions

| | Prediction | Outcome |
|---|---|---|
| P1 | Spread > 60 d for ≥1 group | **Confirmed** (105–147 d for all six) |
| P2 | ≥1 group with both signs | **Confirmed** (all six) |
| P3 | Non-season + pandemic handling > SD multiplier | **Confirmed** (and comparator beats all three) |
| P4 | No group earliest under 100% of specs | **Confirmed** (best is 64.3%) |

All four pre-registered predictions confirmed. P3's margin was larger than expected and surfaced an unanticipated dominant driver (comparator threshold), which is recorded here rather than back-fitted into the plan.

## 7. Files

- `paper3_analysis_plan.md` — the pre-specified plan, unmodified
- `paper3_speccurve.py`, `paper3_inference.py`, `paper3_figure.py`
- `paper3_speccurve.csv` (5,184 estimates), `paper3_dominance.csv` (5,616 rows), `paper3_inference.csv`
- `paper3_fig1_speccurve.png`, `paper3_fig2_allages.png`

## References

Centre for Health Protection. (2026). *Flu Express weekly reports*. https://www.chp.gov.hk

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour, 4*(11), 1208–1214. https://doi.org/10.1038/s41562-020-0912-z
