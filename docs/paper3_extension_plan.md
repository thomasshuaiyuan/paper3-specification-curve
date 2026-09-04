# Paper 3 extension — pre-specified plan

*3 September 2026. Written before either analysis is run. Predictions are scored afterwards
whether or not they hold, following `paper3_analysis_plan.md`.*

Two additions, prompted by the v8 reconciliation of the same date.

---

## Analysis A — baseline anchoring as an eighth dimension

**Motivation.** The v8 diagnostic showed that a baseline built from *the channel's own low half*
inherits that channel's zero fraction, while one built from weeks identified by *an external
reference series* does not. Measured across all 13 channels, threshold height as a percentage of
series maximum spans 29.7-fold under own-series anchoring against 8.6-fold under reference
anchoring, and correlates with zero fraction at ρ = −0.725 (p = 0.005) under the former and
ρ = −0.452 (p = 0.12) under the latter.

The current specification space contains seven tuning choices and no structural one. Anchoring is
structural, it is almost never stated, and it is the choice that reversed a real published claim.

**Implementation.** `ANCHOR ∈ {reference_series, own_series}` added to the existing threshold cross.

- `reference_series` — non-season weeks are those with influenza positivity below quantile *q*;
  each channel is then read on those weeks. This is the current behaviour.
- `own_series` — non-season weeks are those where *that channel* is below its own quantile *q*.
  Each channel therefore gets a different set of weeks. This is the v8 convention.

864 × 2 = **1,728 specifications × 13 channels = 22,464 estimates.** Everything else unchanged.

## Analysis B — a common-dimension subspace across the three families

**Motivation, stated plainly against our own interest.** The manuscript reports that the moving
epidemic method is the most stable of the three families. That comparison is confounded. MEM's
specification space has no analogue of the non-season-quantile sweep (0.25 / 0.40 / 0.50) and a
narrower baseline-statistic sweep, so two of the four largest movers in the threshold family are
absent from MEM's space. R(t) varies neither pandemic-era handling, smoothing, season set, nor the
sustained rule. "Most stable" may partly mean "given fewest ways to move."

A specification-curve paper comparing estimator families across unequal spaces is open to exactly
the critique it makes of others. This analysis closes it.

**Design.** Five dimensions that are shared in kind by all three families, fully crossed and
identical across them:

| Dimension | Levels |
|---|---|
| Comparator threshold | CHP operational (4.94%); derived from the same data |
| Pandemic-era handling | exclude 2020–2022; exclude 2020; retain all |
| Smoothing | none; 3-week centred rolling mean |
| Season set | all 8 seasons; 5 single-wave seasons |
| Sustained rule | 1 week; 2 consecutive weeks |

**48 specifications, run identically for all three families.** For R(t) the sustained rule means
requiring the onset criterion to hold for one or two consecutive weeks.

Family-specific parameters are pinned at a stated reference value and do **not** vary, because they
have no cross-family analogue:

- Threshold crossing: mean + 1.96 SD, non-season quantile 0.40, reference-series anchoring
- MEM: 5 values per training season, arithmetic mean, 95% one-sided limit, pre-peak weeks only
- R(t): serial interval mean 3.0 d SD 2.0, 3-week window, Gamma(1, 0.2) prior, ×10⁴ scaling,
  posterior-mean onset rule

The full-space results already reported answer "how far can this estimate move." This subspace
answers the different and currently unanswered question: "given the same five choices, which family
moves least."

---

## Predictions, recorded before running

**P5.** Anchoring produces a larger swing in mean median-lead than the current largest single
dimension (comparator, 15.3 d).

**P6.** MEM's stability advantage shrinks substantially in the common subspace. Specifically, the
ratio of median spreads (threshold ÷ MEM) falls from its full-space value of 140 / 45.5 ≈ 3.1 to
below 1.55, i.e. more than half the advantage is attributable to unequal specification spaces.

**P7.** R(t) remains the widest-spread family in the common subspace. Its instability is a property
of the estimator, not of how many knobs it was given.

**P8.** Under threshold crossing in the common subspace, the median lead still reverses sign for at
least 7 of 13 channels. The headline dispersion finding is not an artifact of the wide space.

**P9.** Own-series anchoring produces systematically longer apparent leads than reference anchoring,
because it lowers thresholds on zero-inflated channels. Direction stated; magnitude not.

## What each outcome means

- **P6 confirmed.** The manuscript's constructive conclusion is weakened and must be rewritten. The
  honest replacement is that MEM's apparent robustness is substantially an artifact of a narrower
  specification space, with whatever residual advantage survives reported as the real one.
- **P6 refuted.** The conclusion is considerably strengthened, because it survived a test designed
  to break it, and the paper says so.
- **P5 confirmed.** Anchoring becomes the headline dimension and the reporting checklist leads with it.
- **P7 refuted.** The cross-family framing needs rethinking; R(t)'s width would then be an artifact
  of its parameter count rather than the estimator.

No result is a reason to revisit this plan. Deviations, if any are forced, are recorded as
deviations.
