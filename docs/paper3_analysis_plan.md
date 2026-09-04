# Paper 3 — Pre-Specified Analysis Plan

**How sensitive are admissions-based influenza onset lead times to unreported analytic choices? A specification curve analysis of Hong Kong surveillance data, 2014–2026.**

*Written 7 August 2026, before any analysis beyond the exploratory pass that motivated it. The thesis of this paper is that analytic choices drive the reported answer; selecting our own specification after seeing results would refute the paper by demonstration. Everything below is fixed before the curve is computed.*

---

## 1. Motivation

Age-stratified hospital admissions are widely proposed as an early-warning signal for influenza season onset. The standard approach defines an age-specific baseline from "non-season" weeks, sets a threshold some number of standard deviations above it, and reports how many days the crossing precedes an official onset declaration.

Every step of that involves a choice that is rarely stated and never varied: which weeks count as non-season, how many standard deviations, whether pandemic-era weeks contaminate the baseline, whether the series is smoothed, whether one week above threshold counts or several are required, which seasons are included, and what the crossing is compared against.

An exploratory pass over 24 combinations of four of these choices produced median lead times ranging from **−35 to +63 days** for the same age group on the same data. The sign flips. If that holds across a fuller specification space, then published lead times in this literature are not comparable to one another, and a single reported number substantially reflects the analyst rather than the epidemiology.

This is a methodological caution, not a correction of any particular study.

## 2. Data

CHP Flu Express weekly reports, January 2014 – March 2026, 638 weeks (`flux_data.csv`). Publicly available at https://www.chp.gov.hk.

Variables used:

- `AandB_proportion` — combined influenza A and B laboratory positivity, the comparator series
- `Adm_0_5`, `Adm_6_11`, `Adm_12_17`, `Adm_18_49`, `Adm_50_64`, `Adm_65_higher` — influenza-associated admission rates per 10,000 population, 100% complete across the series
- Season windows from `supplementary_table_S1_seasons.csv` (8 influenza seasons flagged `included_in_admissions = Yes`)

No other data source. No neural network. No model fitting of any kind.

## 3. Primary outcome

For each age group *a* and season *s*, under specification *k*:

> **lead**(a, s, k) = (date positivity first exceeds the comparator threshold) − (date `Adm_a` first exceeds its age-specific threshold)

in days. Positive means admissions cross first.

Secondary outcome: **rank**(a, s, k), the ordering of age groups by crossing date, from which we take *which group crosses earliest*.

## 4. The specification space — fixed now

Seven dimensions, fully crossed. Every level is defensible and at least one published study uses it.

| Dimension | Levels | n |
|---|---|---|
| Baseline threshold statistic | mean + 1.645 SD; mean + 1.96 SD; mean + 2.58 SD; 90th percentile; 95th percentile; 97.5th percentile | 6 |
| Non-season definition | positivity below the 25th / 40th / 50th percentile of the series | 3 |
| Pandemic-era handling | exclude 2020–2022; exclude 2020 only; include all weeks | 3 |
| Smoothing | none; 3-week centred rolling mean | 2 |
| Sustained-crossing rule | 1 week above threshold; 2 consecutive weeks | 2 |
| Season set | all 8 admissions-eligible; 5 single-wave only | 2 |
| Comparator threshold | CHP operational 4.94%; data-derived (non-season mean + 1.96 SD, recomputed per specification) | 2 |

**6 × 3 × 3 × 2 × 2 × 2 × 2 = 864 specifications**, each producing a lead time for 6 age groups across up to 8 seasons.

Specifications yielding no crossing for an age group in a season contribute a missing value, and the *proportion of specifications that fail to detect at all* is itself reported.

## 5. Analysis

Following the specification curve method of Simonsohn, Simmons and Nelson (2020):

1. **Descriptive curve.** For each age group, plot all 864 median lead times sorted ascending, with the specification descriptors below, so a reader can see which choices move the estimate.
2. **Dispersion.** Report the median, interquartile range, full range, and the proportion of specifications yielding a positive lead, per age group.
3. **Dominance.** Report the share of specifications under which each age group is the earliest crosser. A group that wins under all specifications is robust; one that wins under a minority is an artifact of the analyst's choices.
4. **Variance decomposition.** Regress lead time on the seven specification dimensions (as factors) to quantify how much of the total variation each choice contributes. This identifies which unreported choice matters most — the practically useful output.
5. **Inference.** Permutation test on the whole curve: shuffle the season labels 1,000 times, recompute the full curve under each shuffle, and compare the observed median absolute lead against the permutation distribution. This asks whether the observed leads are distinguishable from what arbitrary analytic choice would produce on unstructured data.

## 6. Pre-registered predictions

Recorded now so they can be scored honestly afterwards:

- **P1.** The full-range spread of median lead time will exceed 60 days for at least one age group. *(Basis: the exploratory 24-specification pass gave 98 days for 12–17y.)*
- **P2.** At least one age group will yield both positive and negative median leads depending on specification.
- **P3.** The non-season definition and the pandemic-era handling will together account for more of the variance than the SD multiplier — that is, the choice people *do* report matters less than the choices they don't.
- **P4.** No age group will be the earliest crosser under 100% of specifications.

P3 and P4 may well be wrong. The exploratory pass gave 0–5y earliest in 24 of 24, which would falsify P4 if it holds over the larger space.

## 7. What this paper does not claim

- It does not claim any published lead time is incorrect. It quantifies how much that class of estimate moves with analytic choices.
- It does not identify a "correct" specification. There isn't one; that is the point.
- It does not address EpiEstim-based or model-based onset detection. The scope is threshold-crossing on age-stratified admissions.
- It does not establish a causal or biological account of why any age group leads.

## 8. Deviations

Any departure from this plan will be recorded in a dated addendum to this file, with the reason, rather than silently folded into the analysis.

## 9. Target

*Eurosurveillance* or *Epidemiology & Infection*, short communication / surveillance report format.

## References

Centre for Health Protection. (2026). *Flu Express weekly reports*. https://www.chp.gov.hk

Cori, A., Ferguson, N. M., Fraser, C., & Cauchemez, S. (2013). A new framework and software to estimate time-varying reproduction numbers during epidemics. *American Journal of Epidemiology, 178*(9), 1505–1512.

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour, 4*(11), 1208–1214. https://doi.org/10.1038/s41562-020-0912-z

Wang, L., et al. (2009). Review of an influenza surveillance system, Beijing, People's Republic of China. *Emerging Infectious Diseases, 15*(10), 1603–1609.
