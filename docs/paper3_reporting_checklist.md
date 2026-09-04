# A Minimum Reporting Set for Surveillance Onset Lead Times

*Paper 3, prescriptive component. Drafted 7 August 2026 from the 864-specification curve in `paper3_results.md`. Every item is ranked by its measured effect on the reported number, not by opinion.*

---

## Why a checklist, and why these items

Reporting guidelines usually list what seems important. This one lists what was **measured** to move the answer, on 864 fully-crossed specifications of the same Hong Kong CHP data (2014–2026, six age groups, eight influenza seasons).

The result that motivates it: median admissions-based lead time ranges from **−84 to +84 days** across defensible specifications, and the sign flips for every age group. Four analytic choices account for essentially all of that swing. Three of the four are almost never stated in published work.

**The finding that makes this urgent.** The most-favourable specification — the one producing the largest apparent lead — is *identical across all six age groups* on those four levers:

> comparator = operational threshold · pandemic weeks retained in the baseline · non-season = bottom quartile only · low baseline statistic (90th percentile or mean + 1.645 SD)

That combination yields **+84 days** for four of the six age groups. The pooled median across all specifications is **0 to −14 days**. So an analyst who wants age-stratified admissions to look like an early-warning signal has a consistent, reproducible recipe available without doing anything a reviewer could call wrong — and none of the four choices is currently expected to be disclosed.

This is a garden-of-forking-paths problem, not imprecision. The levers are *directional*: each one independently shifts the estimate the same way.

---

## The minimum reporting set

### Tier 1 — must be stated; the estimate is uninterpretable without them

| # | Item | Measured swing | Direction |
|---|---|---|---|
| **1** | **Comparator threshold.** State whether onset is compared against an operational threshold (e.g. CHP's 4.94%) or one derived from the same data, and if derived, give the formula. | **15.3 d** | Operational comparators give leads ~15 d more favourable than data-derived ones (+3.0 d vs −12.3 d pooled). |
| **2** | **Pandemic-era handling.** State whether 2020–2022 weeks are included in the baseline, excluded entirely, or partially excluded. | **14.7 d** | Retaining pandemic weeks depresses the baseline (near-zero admissions under NPIs) and makes crossings look ~15 d earlier (+3.1 d vs −11.6 d). |
| **3** | **Non-season definition.** State the rule used to select baseline weeks — which percentile of the reference series, computed over which period. | **12.8 d** | A stricter non-season window (bottom quartile) gives leads ~13 d more favourable than a median split (+3.0 d vs −9.8 d). |
| **4** | **Baseline statistic.** State the exact threshold rule, including the multiplier or percentile. | **11.8 d** | Lower thresholds cross earlier: 90th percentile vs 97.5th differs by ~12 d (+1.2 d vs −10.6 d). |

Item 2 deserves emphasis for anyone working on post-2020 respiratory surveillance. Including pandemic weeks in a baseline is not a subtle modelling choice — it silently redefines "normal" using a period when the pathogen was absent, and it makes every subsequent signal look early.

### Tier 2 — state for completeness; measured effect is small here

| # | Item | Measured swing |
|---|---|---|
| 5 | Sustained-crossing rule (one week above threshold vs *k* consecutive weeks) | 1.3 d |
| 6 | Smoothing applied to the series before crossing detection | 0.5 d |
| 7 | Season set and the criteria used to select it | 0.1 d |

These matter less than the literature's reporting habits imply. Season set and smoothing are among the most frequently stated choices and moved the estimate least.

### Tier 3 — recommended practice

8. **Report a sensitivity range, not a point estimate.** At minimum, give the lead under the two extreme defensible specifications. Better, report the full specification curve; the code to do so is ~150 lines and is provided.
9. **Report the detection rate**, not only the lead among detected seasons. A specification that only detects onset in half the seasons is not comparable to one that detects in all of them.
10. **Pre-specify before analysis.** The exploratory version of this very analysis used 24 specifications and found one age group earliest in 24 of 24; over 864 specifications that fell to 64%. A small specification space produces over-confident answers — including ours.

---

## Suggested reporting statement

A single sentence discharges Tier 1:

> "Onset was defined as the first week in which the age-specific admission rate exceeded [mean + 1.96 SD] of non-season weeks, where non-season weeks were those with laboratory positivity below the [50th percentile] of the series [excluding 2020–2022], compared against [the CHP operational threshold of 4.94%]. Under the most and least favourable defensible alternatives to these choices, the estimated lead ranges from [X] to [Y] days."

---

## Scope

This applies to threshold-crossing onset detection on age-stratified surveillance series. It has not been tested on R(t)-based onset definitions (EpiEstim or model-based), which have their own specification space — serial interval, window width, prior, and the incidence proxy. Extending the curve to those is the obvious next step and would broaden the checklist accordingly.

## References

Centre for Health Protection. (2026). *Flu Express weekly reports*. https://www.chp.gov.hk

Gelman, A., & Loken, E. (2013). *The garden of forking paths: Why multiple comparisons can be a problem, even when there is no "fishing expedition."* Department of Statistics, Columbia University.

Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science, 22*(11), 1359–1366.

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve analysis. *Nature Human Behaviour, 4*(11), 1208–1214. https://doi.org/10.1038/s41562-020-0912-z
