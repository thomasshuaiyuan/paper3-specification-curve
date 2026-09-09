# FluView replication of the Paper 3 specification curve — pre-specified plan

*4 September 2026. Written before any US estimate had been computed. Section 4 was not revised
after seeing data. Follows `paper3_analysis_plan.md` and `paper3_extension_plan.md`.*

## 1. The question

Paper 3 establishes, on one surveillance system, that onset lead-time estimates reverse sign under
defensible analytic choices and that the largest driver is baseline anchoring, a structural choice
with no standard name. The obvious reviewer question is whether that is a property of analytic
practice or a property of Hong Kong.

This tests it on an independent system: a different agency, different case definitions, a different
population, and a different threshold convention.

**It is a replication, not a new paper.** If it holds, it becomes a Results subsection and a
Limitations deletion. If it fails, that is a finding about the boundary of the claim and is reported
as such.

## 2. Data, verified by query rather than by reading

All from the Delphi Epidata API, tested 4 September 2026.

| Component | Endpoint | Coverage |
|---|---|---|
| Age-stratified influenza hospitalisation rates | `flusurv`, `network_all` | 2009w35 - 2026w20, 549 weeks |
| Laboratory percent positivity (comparator) | `fluview_clinical`, `nat` | 2016w40 - 2026w20, 503 weeks |
| ILI consultation rate and ILI by age | `fluview`, `nat` | 1997w40 - 2026w20, 1,400 weeks |

**Usable overlap: 333 weeks, 10 seasons, 2016/17 to 2025/26.** Granular age channels are 90.7%
complete over that window.

Channels: `rate_age_0tlt1`, `rate_age_1t4`, `rate_age_5t11`, `rate_age_12t17`, `rate_age_18t29`,
`rate_age_30t39`, `rate_age_40t49`, `rate_age_gte75`, `rate_overall`, plus ILINet weighted ILI.
Ten channels against Hong Kong's thirteen.

**Issue pinning.** Delphi exposes `issue` and `lag`, so the data is revisable. The analysis pins a
single issue, recorded with the retrieval date. An unpinned revision would be an unreported analytic
choice in a paper about unreported analytic choices.

## 3. The four things that do not map cleanly, decided now

**Comparator.** CDC publishes an operational baseline for **ILI%**, not for laboratory positivity;
Hong Kong publishes one for positivity (4.94%). There is no one-to-one analogue, so the comparator
dimension takes three levels rather than two: ILINet above the published seasonal baseline;
positivity above a data-derived threshold; ILI% above a data-derived threshold. That two agencies
attach their published threshold to different indicators is itself reportable.

**Reference period.** CDC computes its baseline from the most recent three seasons, rolling. Hong
Kong used a fixed historical pool. This is a dimension the Paper 3 space does not contain, so it is
added here with two levels: rolling three seasons, or all eligible history. If it moves the estimate
materially it belongs in the Hong Kong analysis too, and that will be stated rather than quietly
back-ported.

**Catchment, not population.** FluSurv-NET covers defined catchment areas in 13 states. Hong Kong
admissions are territory-wide. Lead-time *magnitudes* are therefore not comparable between systems;
only *dispersion* is. No cross-system comparison of median lead will be made.

**Pandemic-era handling.** The US season structure matches: peak positivity by season runs 24.7,
27.4, 26.2, 30.3, **0.39** (2020/21), 9.9 (2021/22 rebound), 26.3, 18.2, 31.7, 31.7. The three
pandemic options transfer directly rather than by analogy.

## 4. Specification space

Eight dimensions, as in Hong Kong, with two substitutions.

| Dimension | Levels | n |
|---|---|---|
| Baseline anchoring | reference-series; own-series | 2 |
| Comparator | ILINet vs published baseline; positivity, data-derived; ILI%, data-derived | 3 |
| Baseline statistic | mean + 1.645 / 1.96 / 2.0 / 2.58 SD; 90th, 95th, 97.5th percentile | 7 |
| Non-season definition | positivity below the 25th, 40th, 50th percentile | 3 |
| Reference period | rolling three seasons; all eligible history | 2 |
| Pandemic-era handling | exclude 2020-2022; exclude 2020; retain all | 3 |
| Smoothing | none; 3-week centred | 2 |
| Sustained rule | 1 week; 2 consecutive | 2 |

2 x 3 x 7 x 3 x 2 x 3 x 2 x 2 = **3,024 specifications per channel**.

The baseline statistic gains a 2.0 SD level because that is what CDC actually uses.

## 5. Predictions, recorded before running

**P14.** Baseline anchoring is again the largest single dimension, ahead of the comparator.

**P15.** Own-series anchoring again produces systematically longer apparent leads than reference
anchoring, and the pooled mean again changes sign.

**P16.** The channel most affected by anchoring is again the most zero-inflated one. In FluSurv-NET
that is expected to be `rate_age_12t17`, whose peak rate runs 1.1 to 3.7 per 100,000, so most weeks
sit at 0.0 or 0.1. If confirmed on a different agency's data for the same age group, zero inflation
stops being a Hong Kong curiosity.

**P17.** The median lead reverses sign in at least 7 of 10 channels.

**P18.** The rolling three-season reference period moves the estimate by more than 5 days, making it
a dimension the Hong Kong analysis should have contained.

Predictions are scored whether or not they hold. A prediction that confirms for the wrong reason is
recorded as such.

## 6. What each outcome means

- **P14 and P15 both hold.** Anchoring is a property of analytic practice, not of Hong Kong. Paper 3
  gains a Results subsection and loses its main Limitations item. This is the expected case.
- **P15 fails.** The anchoring effect is system-specific. That is a genuine boundary finding and
  materially weakens the paper's generality claim, which must then be narrowed rather than defended.
- **P16 fails while P15 holds.** Anchoring matters but the mechanism differs between systems. More
  interesting than a clean replication, and it would need its own explanation.
- **P18 holds.** The Hong Kong specification space was incomplete. Report it, and say plainly that
  the US analysis surfaced a dimension the original plan missed.

## 7. Outcome, added after the run

P14 **refuted**: anchoring 5.6 d against the comparator's 14.4 d, fourth of eight rather than first.
P15 **partly confirmed**: own-series anchoring is longer in 10 of 10 channels, but the pooled sign
does not reverse. P16 **refuted** as stated, the largest shift belonging to ILINet weighted ILI,
which has no zero inflation; among the nine hospitalisation channels alone the prediction holds
(`rate_age_12t17` highest on both zero fraction and anchoring shift, Spearman rho = 0.733,
p = 0.025), and that restriction is post-hoc. P17 **confirmed**, 10 of 10. P18 **refuted**, 0.1 d,
so the Hong Kong space was not incomplete in that respect.

The dispersion finding replicates; the ranking of drivers does not. Full results are in
`us/` and Supplementary Note S2 of the manuscript.
