# Paper 3 extension — results against the pre-specified plan

*3 September 2026. Both analyses run exactly as written in `paper3_extension_plan.md`.
No deviations. All five predictions scored.*

## Headline

**The manuscript's constructive conclusion does not survive.** Under equal specification
spaces, the moving epidemic method is not the most stable family — threshold crossing is.
MEM's apparent robustness in the 576-vs-864 comparison was an artifact of a narrower
specification space, which is the paper's own thesis operating on the paper's own analysis.

A different and better claim survives in its place: MEM is the only family whose *direction*
never reverses.

---

## Analysis A — baseline anchoring (1,728 specifications × 13 channels)

**P5 CONFIRMED.** Anchoring is the largest single dimension in the space, ahead of the
comparator threshold that previously held that position.

| Dimension | Swing (days) |
|---|---|
| **Baseline anchoring** | **26.3** |
| Comparator threshold | 18.9 |
| Baseline statistic | 12.2 |
| Non-season definition | 9.8 |
| Season set | 7.3 |
| Pandemic-era handling | 7.1 |
| Sustained-crossing rule | 3.2 |
| Smoothing | 2.8 |

**P9 CONFIRMED.** Own-series anchoring produces systematically longer apparent leads. The
pooled mean median-lead moves from −14.7 days under reference anchoring to +11.6 days under
own-series anchoring — a 26.3-day shift that *reverses the sign of the pooled result*. One
unreported structural choice decides whether these data appear to show early warning at all.

Adding the dimension also takes sign reversal from 12 of 13 channels to **13 of 13**, and the
median spread from 140 to 147 days.

### The mechanism is narrower than predicted, and this is recorded as a partial refutation

The v8 case is explained by zero inflation: 12–17y admissions are 66.6% zeros in their own
low half, and their own-series threshold sits at 2.8% of series maximum against 10.4% under
reference anchoring, a 3.75-fold difference.

The generalisation across channels holds for *relative threshold height* but not for *days*:

- zero fraction vs threshold ratio (reference ÷ own): ρ = 0.570, **p = 0.042**
- zero fraction vs anchoring shift in days: ρ = −0.470, p = 0.105, and in the opposite
  direction to the naive prediction

Zero inflation reliably lowers the bar in relative terms. How many days that buys depends on
how steeply the channel rises through the threshold, which is a separate property. The largest
day-shifts are in traditional medicine (+65.3), care-home fever (+60.1) and school outbreaks
(+51.9), two of which have essentially no zeros. **Anchoring matters everywhere; zero
inflation is the mechanism in the v8 case specifically, not a general law.**

---

## Analysis B — common-dimension subspace (48 shared specifications, three families)

Five choices, identical across families: comparator, pandemic-era handling, smoothing, season
set, sustained rule. Family-specific parameters pinned at stated reference values.

| Family | Median spread | Range | Sign reverses |
|---|---|---|---|
| Threshold crossing | **35.0 d** | 21.0 – 101.5 | 7 of 13 |
| Moving epidemic method | 49.0 d | 31.5 – 91.0 | **0 of 13** |
| R(t), renewal equation | 77.0 d | 56.0 – 140.0 | 13 of 13 |

**P6 CONFIRMED, and then some.** The prediction was that the threshold ÷ MEM spread ratio
would fall from 3.08 to below 1.55. It fell to **0.71** — the ordering reversed. On equal
terms threshold crossing is the *more* stable of the two.

**P7 CONFIRMED.** R(t) remains the widest family, at more than twice the threshold spread,
and reverses sign in every channel. Its instability is a property of the estimator, not of
how many parameters it was given.

**P8 CONFIRMED.** Threshold crossing still reverses sign in 7 of 13 channels within a
48-specification subspace containing none of the baseline-construction choices. The core
dispersion finding is not an artifact of a wide space.

### What replaces the discarded conclusion

MEM does not produce the narrowest estimates. It produces the only *directionally consistent*
ones: 0 of 13 channels reverse sign, against 7 of 13 for threshold crossing and 13 of 13 for
R(t). Under every one of the 48 shared specifications, MEM says no channel in this system
leads laboratory positivity.

That is a more useful property than a narrow spread, and it is the one an agency needs. The
qualitative conclusion is stable even though the magnitude is not. The revised claim is that
MEM is robust in what it concludes and no more precise than anything else in how much.

### The finding this produces about the paper itself

The full-space comparison gave MEM a 3.08-fold stability advantage. The equal-space
comparison reverses it. Nothing about the data or the methods changed — only how many ways
each family was allowed to vary, which is an analytic choice we made and did not report.

The paper's thesis, applied to the paper, holds. This should be stated in the manuscript
rather than quietly fixed, because a specification-curve paper that concealed a specification
artifact in its own headline comparison would be worth very little.

---

## Scored predictions

| | Prediction | Outcome |
|---|---|---|
| P5 | Anchoring swing > comparator (15.3 d) | **Confirmed** — 26.3 d vs 18.9 d |
| P6 | Threshold ÷ MEM spread ratio falls below 1.55 | **Confirmed** — 3.08 → 0.71, ordering reversed |
| P7 | R(t) widest in the common subspace | **Confirmed** — 77.0 d |
| P8 | Threshold sign reverses in ≥ 7 of 13 channels | **Confirmed** — exactly 7 of 13 |
| P9 | Own-series anchoring gives longer leads | **Confirmed** — +26.3 d, pooled sign reverses |

Five for five, with one sub-hypothesis (zero inflation as the general mechanism for the
anchoring effect) refuted and recorded above rather than dropped.

## Files

- `paper3_anchor_speccurve.py` → `paper3_anchor_speccurve.csv` (22,464 estimates)
- `paper3_common_subspace.py` → `paper3_common_subspace.csv` (1,872 estimates)
- `paper3_extension_plan.md` — the plan, unmodified
