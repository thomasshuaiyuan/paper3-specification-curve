**Whether a surveillance signal appears to lead laboratory positivity in influenza onset detection is determined by analytic choice and by method family: a specification curve analysis of thirteen channels and three estimator classes, Hong Kong, 2014–2026**

**Thomas Yuan**^1,2^, **Vijaykrishna Dhanasekaran**^1,\*^

^1^ School of Public Health, LKS Faculty of Medicine, The University of Hong Kong & HKU-Pasteur Research Pole, Hong Kong SAR, China

^2^ Department of Epidemiology, Mailman School of Public Health, Columbia University, New York, NY, USA

\* Corresponding author: veej@hku.hk

*DRAFT v1, 8 August 2026. Target: Eurosurveillance, Research article (≤3,500 words, ≤6 illustrations, 15–30 references).*

---

# Abstract

**Background.** Hospital admissions and similar signals are widely proposed as early-warning indicators for influenza season onset. Estimating how far they lead an onset declaration requires analytic decisions that are rarely reported.

**Aim.** To quantify how much the estimated lead time depends on those decisions, and identify which a reader needs.

**Methods.** We analysed 638 weeks of Centre for Health Protection Flu Express data from Hong Kong (January 2014 to March 2026), covering 13 surveillance channels and eight influenza seasons. Analytic choices were fully crossed for three onset-detection families — threshold crossing, the moving epidemic method, and R(t) by the renewal equation — giving 576 to 1,728 specifications per channel per family. All three were also run over an identical 48-specification subspace of the choices they share, comparing their stability on equal terms.

**Results.** Median lead reverses sign in all 13 channels and a signal leads in only 14% to 37% of threshold specifications. The largest driver is baseline anchoring, at 26.3 days: whether non-season weeks come from laboratory positivity or from each channel's own distribution decides the sign of the pooled result. R(t) disagrees with both magnitude-based families, the same channels leading in 73% to 100% of its specifications. On the equal-terms subspace MEM is not the narrowest family but is the only one that never reverses direction.

**Conclusion.** Whether a surveillance signal appears to provide early warning depends more on unreported analytic choices, and on the estimator class, than on the data. We propose a minimum reporting set.

---

# Introduction

Public health agencies declare influenza season onset when a surveillance indicator crosses a threshold. In Hong Kong the Centre for Health Protection (CHP) uses laboratory positivity for influenza A and B; systems in Europe and the United States use influenza-like illness consultation rates with thresholds set by the moving epidemic method or by regression on historical baselines [1,2], within the standards published by the World Health Organization [3].

Because positivity is a lagging indicator of transmission, signals that might cross earlier attract interest. Paediatric and adolescent hospital admissions have been proposed as sentinel signals, on the argument that school-age contact patterns amplify transmission before it is visible in laboratory data [4,5]. Multi-stream work in Hong Kong has integrated outpatient and school absenteeism data for situational awareness [6].

Evaluating such a claim requires a lead time: the interval between a candidate series crossing its own threshold and the reference indicator crossing its threshold. Producing that number involves at least eight decisions, covering how non-season weeks are identified and from which series, what statistic sets the threshold, how pandemic weeks are handled, whether the series is smoothed, how many weeks above threshold are required, which seasons are analysed, and what the crossing is compared against. None is wrong, each has published precedent, and all but the threshold statistic are seldom stated.

Fields that have examined this flexibility find it consequential. Simmons et al. [7] showed that undisclosed flexibility can produce apparently significant findings from null data, and Gelman and Loken [8] described the same problem where no explicit search occurs. Multiverse [9] and specification curve analysis [10] compute the estimate under every reasonable specification; applied to adolescent well-being, that showed reported effect sizes spanning the range obtainable by analytic choice alone [11].

A second source of flexibility sits above the analytic one. Onset can be defined by threshold crossing, by the moving epidemic method, or by R(t) crossing 1. These do not mark the same event: R(t) > 1 identifies when growth begins, the other two when magnitude has accumulated. All three are in use and lead times from them are compared as though they were one quantity.

Surveillance has not been examined this way, though its pipelines contain comparable flexibility and its outputs inform operational decisions. We apply specification curve analysis to influenza onset lead times in Hong Kong, across every channel the system collects and all three families, and use the result to propose what such analyses should report.

# Methods

## Data

Weekly CHP Flu Express reports covering January 2014 to March 2026 provide 638 weeks of publicly available surveillance data [12]. Combined influenza A and B laboratory positivity is the reference indicator. As candidate signals we use every channel complete and non-degenerate across the study seasons: influenza-associated hospital admission rates per 10,000 population for all ages and six age strata (0–5, 6–11, 12–17, 18–49, 50–64, 65 and above), influenza-like illness consultation rates from private general practitioners, emergency departments and Chinese medicine practitioners, school and non-school outbreak counts, and residential care home fever surveillance. This gives 13 channels spanning six data-generating processes.

Three channels were excluded for incompleteness: family medicine consultations, severe case counts and kindergarten fever surveillance, each usable in 4 or fewer of the 8 seasons. No other data source was used and no model was fitted. The six age-stratified admission series are reported separately in Supplementary Table S1.

## Outcome

For channel *c*, season *s* and specification *k*, the lead is the interval in days between the date positivity first exceeds the comparator threshold and the date channel *c* first exceeds its own. Positive values indicate the candidate signal crosses first. The summary quantity is the median lead across seasons within a specification.

## Specification space

Eight dimensions were crossed completely (Table 1). Levels were fixed before analysis and each has published precedent, yielding 6 × 3 × 3 × 2 × 2 × 2 × 2 × 2 = 1,728 specifications per channel and 22,464 estimates across all 13.

Anchoring is structural rather than a tuning choice, and is the one dimension not in the original plan. Under reference anchoring, non-season weeks are those in which laboratory positivity falls below the chosen quantile and every channel is read on that same set. Under own-series anchoring each channel supplies its own non-season weeks from its own low quantile, so every baseline uses a different set. Both conventions appear in published analyses, usually unnamed.

## R(t)-based onset detection

The second family estimates the effective reproduction number by the renewal-equation approach of Cori et al. [13], implemented directly so every choice is explicit. With prior R ~ Gamma(*a*, scale *b*), incidence *I*, total infectiousness Λ*~s~* = Σ*~k~ I~s−k~ w~k~*, and a window τ ending at week *t*, the posterior is Gamma with shape *a* + Σ*~τ~ I~s~* and rate 1/*b* + Σ*~τ~* Λ*~s~*. Onset is the first week the chosen criterion rises above 1.

Seven dimensions were crossed, again giving 864 specifications per channel: serial interval mean (2, 3, 4 days), spanning the range reported for influenza [14], and standard deviation (1, 2 days); estimation window (2, 3, 4, 6 weeks); prior (Gamma(1, 0.2), Gamma(0.001, 0.001), Gamma(1, 5)); incidence proxy scaling (×10^3^, ×10^4^, ×10^5^); onset rule (posterior mean > 1, or posterior 2.5th percentile > 1); and the same two comparator thresholds.

Scaling is an explicit dimension rather than a preprocessing detail because the posterior is not scale-invariant: multiplying incidence by a constant scales both sums, so the prior washes out as the multiplier grows. Surveillance series are converted to pseudo-incidence by multipliers chosen for convenience, often differing between channels in one analysis.

## The moving epidemic method

The third family is the moving epidemic method (MEM), used by ECDC and many national systems [1]. From historical seasons the *n* highest non-epidemic values are pooled and the pre-epidemic threshold is the upper limit of a one-sided confidence interval around their mean; onset is the first week the target season exceeds it. Thresholds were computed leave-one-out.

Published applications disagree on the details, and those disagreements form the specification space: values taken per season (3, 5, 8, 12); arithmetic or geometric mean; confidence level (90%, 95%, 99%); one week above threshold or two consecutive; non-epidemic values from before the seasonal peak only or from both sides; the same three pandemic-era options; and the same two comparators, giving 576 specifications per channel.

Our implementation approximates rather than reproduces the `mem` R package, which selects each season's epidemic period by an iterative MAP-curve procedure where we treat the weeks within two of the peak as epidemic. Results characterise the family, not any particular implementation.

## Comparing families on equal terms

Spreads are not comparable across families whose specification spaces differ in size, and ours do: the MEM space contains no analogue of the non-season quantile sweep, and the R(t) space varies neither pandemic-era handling, smoothing, season set nor the sustained rule. A family given fewer ways to move will move less. We therefore also ran all three over an identical subspace of the five choices they share in kind — comparator, pandemic-era handling, smoothing, season set and the sustained rule — giving 48 specifications per family per channel, with family-specific parameters pinned at stated reference values (Supplementary Table S3). The full spaces answer how far each estimate can move; this subspace answers which family moves least given the same choices.

## Analysis

The analysis plan, including the specification space and four predictions, was written before the curve was computed and is available with the code. The anchoring dimension and the equal-terms comparison were added later, under a second pre-specified plan with five further predictions, also available with the code. Specifications in which a channel never crosses contribute a missing value, and the count of such specifications is reported.

We report the distribution of median lead across specifications, the proportion yielding a positive lead, and the proportion with no crossing. Each dimension's contribution is summarised by the swing in mean median-lead between its extreme levels. Analyses used Python 3.11; code and full specification-level output are at the repository listed under Data availability.

# Results

## The estimate spans its own plausible range

Across 1,728 specifications the median lead time ranges from −84 to +84 days (Supplementary Table S1), and every age group produces both positive and negative median leads. The narrowest range, for the 0–5 year group, still spans 105 days; the widest, for 12–17 years, 154. Figure 1 shows the specification curve for private outpatient consultations with the analytic choices beneath it; Supplementary Figure S1 shows the age-stratified admission series separately.

Admissions cross before positivity in 17.6% of specifications for the 12–17 year group, rising to 32.1% for 6–11 years. Under most defensible analyses of these data, age-stratified admissions cross their own baseline after positivity has already crossed the operational threshold, not before.

## Baseline anchoring dominates every other choice

Table 2 gives the swing attributable to each dimension. Baseline anchoring is the largest at 26.3 days, ahead of the comparator threshold at 18.9, the baseline statistic at 12.2 and the non-season definition at 9.8; smoothing and the sustained rule contribute under 4 days each.

The anchoring effect is directional and large enough to reverse the pooled result. Mean median-lead is −14.7 days under reference anchoring and +11.6 under own-series anchoring, so one unstated structural choice decides whether these data appear to show early warning at all. It also takes sign reversal from 12 of 13 channels to all 13.

The mechanism is that own-series anchoring lets a channel's own low values set its bar, and zero-inflated series benefit most in relative terms: the fraction of weeks at zero within a channel's low half predicts how far its threshold falls (ρ = 0.570, p = 0.042), though not the shift in days (ρ = −0.470, p = 0.105), which also depends on how steeply the channel rises through the bar.

The influential choices also compound: the specification producing the largest apparent lead is identical across age groups (own-series anchoring, operational comparator, pandemic weeks retained, non-season restricted to the lowest quartile, a low baseline statistic), and yields +84 days for four of six groups against a pooled median of 0 to −7. Pandemic weeks contribute because influenza circulation fell to near zero under non-pharmaceutical interventions, so retaining them lowers a baseline's level and variance together [15].

The ordering of the remaining dimensions is close to the inverse of current reporting practice: season set and smoothing are among the most often stated and move the estimate least, while the comparator and the anchoring convention, which contribute most, are frequently implicit or absent.

## The instability is not specific to hospital admissions

Across all 13 channels, 22,464 estimates (Figure 2, Supplementary Table S2), the sign of the median lead reverses in every one. Ranges span 105 days for 0–5 year admissions to 217 for care-home fever, and the two widest belong to non-admissions channels.

Aggregating by data-generating process, a signal crosses before positivity in 33.5% of specifications for traditional medicine consultations and 23.4% to 25.5% for each of the other five. Early crossing is a minority result for every signal family Hong Kong collects, and differences between families are smaller than differences within any one.

Restricting to reference anchoring reproduces the original seven-dimension analysis exactly — sign reversal in 12 of 13 channels, spreads of 105 to 189 days, positive leads in 0% to 20.6% — so the changes above are attributable to the added dimension alone.

## R(t)-based onset reverses the direction of the finding

R(t)-based onset produces the opposite answer (Figure 3, Table 3): under threshold crossing a signal leads positivity in 14% to 37% of specifications, under R(t) in 73% to 100%, and the disagreement holds for all 13 channels.

Part of this gap is definitional: R(t) > 1 marks the onset of growth whereas a threshold marks accumulated magnitude, so a growth criterion fires earlier on the same series. That is a reason to avoid comparing lead times across families, not to prefer one.

The families are sensitive to different choices. For R(t) the ranking is prior (23.0 days), estimation window (19.5) and incidence scaling (12.4), while the comparator contributes 0.5 and the serial interval 0.2, the last consistent with weekly data giving roughly one observation per influenza generation. R(t) spreads are wide but uneven: three outpatient channels span only 28 days, while the 12–17 year admission series spans 364, the widest of any channel under any family. The scaling effect is concentrated in the vague Gamma(0.001, 0.001) prior, under which the multiplier alone moves the mean median-lead by 41 days (Supplementary Note S1); a vague prior is adopted to avoid influencing the result and on pseudo-incidence does the opposite.

## The operational method is directionally stable, not narrow

MEM behaves differently again (Figure 3, Table 3). Across its own 576 specifications the spreads run from 28 to 80 days, median 45.5, against 140 for threshold crossing and 77 for R(t); the sign reverses in only 1 of 13 channels, and in 12 of 13 no specification yields a positive lead at all.

That advantage does not survive an equal-terms comparison (Table 2b). Over the 48 shared specifications the median spread is 35.0 days for threshold crossing, 49.0 for MEM and 77.0 for R(t): the ordering of the first two reverses. Two of the four largest movers in the threshold family have no analogue in the MEM space, so the original comparison rewarded MEM for having fewer ways to move.

What survives is a different and more useful property. MEM is the only family whose direction never reverses: 0 of 13 channels change sign across the shared specifications, against 7 of 13 for threshold crossing and 13 of 13 for R(t). Under every one of the 48 it reports that no channel in this system leads laboratory positivity. It is robust in what it concludes and no more precise than the others in how much. Its own influential choices are the values taken per season (15.7 days) and whether non-epidemic values come from before the peak only or both sides (12.4 days), while comparator and confidence level contribute 1.6 each.

R(t) is widest under both treatments, reversing sign in every channel, so its instability is a property of the estimator rather than of its parameter count. Threshold crossing still reverses sign in 7 of 13 channels within a subspace containing none of the baseline-construction choices, so the dispersion finding is not an artifact of a wide space either.

## Published estimates fall inside the specification range

Two published estimates of the same quantity can be placed on the curve directly.

Schanzer et al. [17] report hospitalisations leading laboratory-positive tests by 1.6 days (95% CI −1.5 to 4.7) across 28 Canadian regional seasons; their interval spans 37% of our specifications. White et al. [18] found electronic laboratory reporting leading admissions by one to two weeks in California, a window containing 39% of our all-ages specifications, with neither threshold nor baseline reported. Both fall inside the range obtainable by analytic choice alone and both side with the magnitude-based families. This is a convenience sample of two, not a systematic review.

## Restricting to a core specification set

Within the reference-anchored half of the space, excluding specifications that stack more than two extreme choices retains 688 of 864 (80%). The sign still reverses in 12 of 13 channels and the median spread falls only from 140 to 112 days, so the instability is not an artifact of implausible corners. This and the operational analysis below use reference anchoring, the conservative half.

## The choice has operational consequences

For 0–5 year admissions under core specifications, the median gap between the earliest and latest defensible onset declaration is **11.5 weeks**, the maximum 33 (2016/17). Only 2023/24 shows complete agreement across all 212 core specifications; in the remaining seven an agency could have declared onset anywhere in a 5 to 33 week window.

# Discussion

Four findings follow from these data.

First, a reported admissions-based lead time carries little information without its specification. The estimate spans 105 to 154 days depending on age group, and reverses sign, on one surveillance system with complete data and no modelling.

Second, the choices that matter are not the ones reported, and the largest has no name in this literature. Whether a baseline is anchored to an external reference series or to the channel's own distribution moves the estimate by 26 days and reverses the pooled sign, yet is almost never stated. The comparator threshold follows. Smoothing, the sustained rule and season selection are stated more often and matter far less.

Third, the influential choices are directional and mutually reinforcing, which distinguishes this from ordinary imprecision. An analyst preferring a favourable conclusion has four levers worth roughly four, three, two and one and a half weeks, all pushing the same way, none requiring a step a reviewer would call wrong. This is the garden-of-forking-paths structure [8], arising in surveillance rather than in an experiment.

Fourth, the estimator class matters at least as much as the choices within it, but not in the way a naive comparison suggests. On its own space the moving epidemic method looked much the most stable; given the same five choices as the others it is not, because its published space contains fewer of the dimensions that move estimates. What survives is that MEM alone never reverses direction, which is robustness in the conclusion rather than precision in the magnitude, and is the property an agency deciding whether to act needs.

That correction is the paper's own argument turned on itself. Nothing about the data or the methods changed between the two comparisons, only how many ways each family was permitted to vary, which was our choice and went unreported. We state it rather than quietly fixing it, because a specification-curve analysis concealing a specification artifact in its own headline comparison would be worth little.

We do not claim any published lead time is incorrect, and this analysis cannot identify a correct specification. None arises from these data; that is the point. What follows is a reporting requirement.

## A minimum reporting set

Analyses reporting onset lead times should state, at minimum, the items measured here to move the estimate.

For threshold crossing, in order of measured effect: the baseline anchoring, meaning whether non-season weeks are identified from an external reference series or from the channel's own distribution; the comparator threshold and whether it is operational or derived from the same data; the baseline statistic; the rule defining non-season weeks; and the handling of pandemic-period weeks. Two free diagnostics would have caught the anchoring problem before it reached a manuscript: the fraction of weeks at zero within each channel's baseline window, and the resulting threshold as a percentage of that channel's series maximum.

For R(t)-based onset: the prior and its parameterisation, the estimation window, the multiplier converting the proportion to pseudo-incidence, and the onset criterion. The serial interval, almost always reported, moved the estimate by under one day at weekly resolution. For MEM: the values taken from each training season and whether non-epidemic weeks come from before the peak only or from both sides, worth 15.7 and 12.4 days, against under 2 for the confidence level and mean type that published descriptions do specify.

Lead times from different families should not be pooled, because R(t) > 1 and a magnitude threshold mark different events. A sensitivity range under the extreme defensible alternatives should accompany the point estimate, and the detection rate should be reported alongside the lead. These are narrower instances of the reporting practices set out in the reproducibility literature [16].

## Limitations

This analysis covers one surveillance system, one pathogen and eight seasons, though it spans 13 channels, six data-generating processes and three estimator families. Whether the magnitudes replicate elsewhere is untested, and two external estimates are not a survey. The specification space, though larger than usual, remains a subset of defensible analyses; dimensions we did not vary would add variation rather than reduce it, as anchoring did. Our MEM is a reimplementation rather than the `mem` package, and mechanistic-model onset definitions were not examined. Finally, this is descriptive of estimator behaviour and makes no claim about whether any age group is biologically an early amplifier of transmission.

# Conclusion

On Hong Kong surveillance data, whether a signal appears to lead laboratory positivity in influenza onset detection is determined more by unreported analytic choices than by the data. The estimate reverses sign for every channel examined, and the largest single driver, whether the baseline is anchored to a reference series or to the channel's own distribution, has no standard name and is almost never stated. Comparisons between estimator families are themselves sensitive to how many choices each family is given; on equal terms the method agencies already use is the only one that never reverses direction, though no more precise than the alternatives. Reporting these choices is inexpensive and would make such estimates comparable across studies for the first time.

# Tables

**Table 1.** The threshold-crossing specification space. Eight analytic dimensions, fully crossed, giving 1,728 specifications per channel.

| Dimension | Levels | n |
|---|---|---|
| Baseline statistic | mean + 1.645 SD; mean + 1.96 SD; mean + 2.58 SD; 90th, 95th, 97.5th percentile | 6 |
| Non-season definition | positivity below the 25th, 40th or 50th percentile of the series | 3 |
| Pandemic-era handling | exclude 2020–2022; exclude 2020 only; retain all weeks | 3 |
| Smoothing | none; 3-week centred rolling mean | 2 |
| Sustained-crossing rule | 1 week above threshold; 2 consecutive weeks | 2 |
| Season set | all 8 admissions-eligible seasons; 5 single-wave seasons | 2 |
| Comparator threshold | CHP operational (4.94%); derived from the same data | 2 |
| Baseline anchoring | non-season weeks set by laboratory positivity; set by the channel's own low quantile | 2 |

**Table 2.** Swing in mean median-lead attributable to each analytic dimension, threshold crossing, pooled across the 13 channels.

| Dimension | Levels compared | Swing (days) |
|---|---|---|
| **Baseline anchoring** | non-season weeks from laboratory positivity vs from the channel's own low quantile | **26.3** |
| Comparator threshold | operational (CHP 4.94%) vs derived from the same data | 18.9 |
| Baseline statistic | mean + 1.645/1.96/2.58 SD vs 90th/95th/97.5th percentile | 12.2 |
| Non-season definition | below the 25th vs 40th vs 50th percentile | 9.8 |
| Season set | all 8 seasons vs 5 single-wave seasons | 7.3 |
| Pandemic-era handling | exclude 2020–2022 vs exclude 2020 only vs retain all | 7.1 |
| Sustained-crossing rule | 1 week vs 2 consecutive weeks | 3.2 |
| Smoothing | none vs 3-week centred rolling mean | 2.8 |

**Table 2b.** The three families over an identical 48-specification subspace of the five choices they share.

| Family | Median spread | Range across channels | Sign reverses |
|---|---|---|---|
| Threshold crossing | 35.0 d | 21.0–101.5 | 7 of 13 |
| Moving epidemic method | 49.0 d | 31.5–91.0 | **0 of 13** |
| R(t), renewal equation | 77.0 d | 56.0–140.0 | 13 of 13 |


**Table 3.** Three onset-detection families, same channels and same data. Median lead in days, share of specifications yielding a positive lead, and full spread.

| Channel | Thr median | Thr % pos | Thr spread | MEM median | MEM % pos | MEM spread | R(t) median | R(t) % pos | R(t) spread |
|---|---|---|---|---|---|---|---|---|---|
| Outpatient (private GP) | −7 | 23.4 | 186 | −42 | 0.0 | 70 | +46 | 100.0 | 28 |
| Emergency attendance | −9 | 23.6 | 200 | −32 | 0.0 | 35 | +38 | 100.0 | 28 |
| Traditional medicine | 0 | 33.5 | 196 | −28 | 6.2 | 80 | +38 | 88.9 | 102 |
| School outbreaks | −7 | 36.7 | 182 | −35 | 0.0 | 63 | +28 | 100.0 | 28 |
| Non-school outbreaks | −7 | 14.2 | 147 | −28 | 0.0 | 42 | +10 | 94.4 | 63 |
| Care-home fever | −4 | 24.1 | 217 | −21 | 0.0 | 56 | +21 | 73.4 | 122 |
| Admissions, all ages | 0 | 19.9 | 133 | −21 | 0.0 | 28 | +24 | 80.0 | 154 |
| Admissions 0–5y | 0 | 22.4 | 105 | −21 | 0.0 | 52 | +24 | 88.9 | 77 |
| Admissions 6–11y | 0 | 32.1 | 133 | −28 | 0.0 | 49 | +24 | 88.9 | 140 |
| Admissions 12–17y | −7 | 17.6 | 154 | −28 | 0.0 | 28 | +24 | 83.2 | 364 |
| Admissions 18–49y | 0 | 26.8 | 140 | −28 | 0.0 | 42 | +24 | 84.4 | 77 |
| Admissions 50–64y | 0 | 28.1 | 140 | −24 | 0.0 | 35 | +21 | 87.3 | 94 |
| Admissions 65+y | 0 | 23.1 | 140 | −24 | 0.0 | 46 | +24 | 78.5 | 70 |



# Figures

**Figure 1.** Specification curve for private outpatient consultations. Upper panel: median lead time under each of 1,728 threshold-crossing specifications, sorted ascending; blue indicates the signal crossing before laboratory positivity, orange after. Lower panel: the analytic choices producing each specification.

![Figure 1](paper3_fig1_speccurve.png)

**Figure 2.** Range of median lead time across 1,728 specifications for all 13 surveillance channels under threshold crossing. Orange indicates specifications under which laboratory positivity crosses first, blue those under which the signal crosses first. The sign reverses in all 13 channels.

![Figure 2](paper3_fig3_allchannels.png)

**Figure 3.** Threshold crossing (orange), the moving epidemic method (aqua) and R(t)-based onset (blue), same channels and same data, 576 to 1,728 specifications per family. Percentages give the share of specifications yielding a positive lead. The two magnitude-based families agree; R(t) disagrees on the direction for every channel.

![Figure 3](paper3_fig4_method_families.png)

# Supplementary material

**Supplementary Table S1.** Distribution of median lead time (days) across 1,728 threshold-crossing specifications, six age-stratified admission series. Positive values indicate that admissions cross before laboratory positivity.

| Age group (years) | Median | IQR | Range | Spread | Positive lead (% of specifications) |
|---|---|---|---|---|---|
| 0–5 | 0 | 0 to 0 | −21 to +84 | 105 | 22.4 |
| 6–11 | 0 | −7 to +7 | −49 to +84 | 133 | 32.1 |
| 12–17 | −7 | −18 to 0 | −84 to +70 | 154 | 17.6 |
| 18–49 | 0 | −7 to +4 | −56 to +84 | 140 | 26.8 |
| 50–64 | 0 | 0 to +7 | −56 to +84 | 140 | 28.1 |
| 65+ | 0 | −7 to 0 | −56 to +84 | 140 | 23.1 |


**Supplementary Table S2.** Distribution of median lead time (days) across 1,728 threshold-crossing specifications, all 13 surveillance channels. "Not estimable" counts specifications in which the channel never crosses its threshold in any season.

| Channel | Family | Median | Range | Spread | Positive lead (%) | Not estimable |
|---|---|---|---|---|---|---|
| Outpatient (private GP) | Outpatient | −7 | −102 to +84 | 186 | 23.4 | 0 |
| Emergency attendance | Emergency | −9 | −116 to +84 | 200 | 23.6 | 0 |
| Traditional medicine | Traditional medicine | 0 | −112 to +84 | 196 | 33.5 | 0 |
| School outbreaks | Institutional outbreak | −7 | −98 to +84 | 182 | 36.7 | 0 |
| Non-school outbreaks | Institutional outbreak | −7 | −91 to +56 | 147 | 14.2 | 0 |
| Care-home fever | Care-home fever | −4 | −133 to +84 | 217 | 24.1 | 332 |
| Admissions, all ages | Hospital admissions | 0 | −49 to +84 | 133 | 19.9 | 0 |
| Admissions 0–5y | Hospital admissions | 0 | −21 to +84 | 105 | 22.4 | 0 |
| Admissions 6–11y | Hospital admissions | 0 | −49 to +84 | 133 | 32.1 | 0 |
| Admissions 12–17y | Hospital admissions | −7 | −84 to +70 | 154 | 17.6 | 96 |
| Admissions 18–49y | Hospital admissions | 0 | −56 to +84 | 140 | 26.8 | 0 |
| Admissions 50–64y | Hospital admissions | 0 | −56 to +84 | 140 | 28.1 | 0 |
| Admissions 65+y | Hospital admissions | 0 | −56 to +84 | 140 | 23.1 | 0 |

**Supplementary Table S3.** Reference values at which family-specific parameters were pinned for the equal-terms comparison.

| Family | Pinned parameters |
|---|---|
| Threshold crossing | mean + 1.96 SD; non-season quantile 0.40; reference-series anchoring |
| Moving epidemic method | 5 values per training season; arithmetic mean; 95% one-sided limit; pre-peak weeks only |
| R(t), renewal equation | serial interval mean 3.0 d, SD 2.0; 3-week window; Gamma(1, 0.2) prior; ×10⁴ scaling; posterior-mean rule |

**Supplementary Note S1.** Under the informative priors the incidence multiplier moves the mean median-lead by under 4 days. Under the vague Gamma(0.001, 0.001) prior it moves it from −15.6 to +25.4 days as the multiplier increases from 10^3^ to 10^5^, a 41-day swing from an arbitrary constant. Analyses converting proportions to pseudo-counts should report the multiplier alongside the prior, or verify that the pairing is scale-invariant over the range used.

**Supplementary Figure S1.** Specification curves for all six age-stratified admission series individually under threshold crossing.

![Supplementary Figure S1](paper3_fig2_allages.png)

# Data availability

CHP Flu Express data are publicly available at https://www.chp.gov.hk. Analysis code, the pre-specified analysis plan and specification-level output are available at [repository URL to be added].

# Ethics

Analysis of aggregated, publicly available surveillance data with no individual-level information. [Formal exemption determination and determining body to be named.]

# Funding

[To be added.]

# Author contributions

[TY designed and conducted the analyses and wrote the manuscript. VD supervised, provided critical feedback and revised the manuscript.]

# Competing interests

The authors declare no competing interests.

---

# References

1. Vega T, Lozano JE, Meerhoff T, Snacken R, Mott J, Ortiz de Lejarazu R, et al. Influenza surveillance in Europe: establishing epidemic thresholds by the moving epidemic method. Influenza Other Respir Viruses. 2013;7(4):546–558.

2. Centers for Disease Control and Prevention. U.S. influenza surveillance: purpose and methods. Atlanta: CDC; 2025. Available from: https://www.cdc.gov/fluview/overview/index.html

3. World Health Organization. Global epidemiological surveillance standards for influenza. Geneva: WHO; 2013.

4. Wang L, Chu Y, Zhang S, Wang Q, Wu S, Yang P, et al. Review of an influenza surveillance system, Beijing, People's Republic of China. Emerg Infect Dis. 2009;15(10):1603–1609.

5. Mossong J, Hens N, Jit M, Beutels P, Auranen K, Mikolajczyk R, et al. Social contacts and mixing patterns relevant to the spread of infectious diseases. PLoS Med. 2008;5(3):e74.

6. Lau EHY, Cheng CKY, Ip DKM, Cowling BJ. Situational awareness of influenza activity based on multiple streams of surveillance data using multivariate dynamic linear model. PLoS One. 2012;7(5):e38346.

7. Simmons JP, Nelson LD, Simonsohn U. False-positive psychology: undisclosed flexibility in data collection and analysis allows presenting anything as significant. Psychol Sci. 2011;22(11):1359–1366.

8. Gelman A, Loken E. The garden of forking paths: why multiple comparisons can be a problem, even when there is no "fishing expedition" or "p-hacking" and the research hypothesis was posited ahead of time. New York: Department of Statistics, Columbia University; 2013.

9. Steegen S, Tuerlinckx F, Gelman A, Vanpaemel W. Increasing transparency through a multiverse analysis. Perspect Psychol Sci. 2016;11(5):702–712.

10. Simonsohn U, Simmons JP, Nelson LD. Specification curve analysis. Nat Hum Behav. 2020;4(11):1208–1214.

11. Orben A, Przybylski AK. The association between adolescent well-being and digital technology use. Nat Hum Behav. 2019;3(2):173–182.

12. Centre for Health Protection. Flu Express weekly reports. Hong Kong SAR: CHP; 2026. Available from: https://www.chp.gov.hk

13. Cori A, Ferguson NM, Fraser C, Cauchemez S. A new framework and software to estimate time-varying reproduction numbers during epidemics. Am J Epidemiol. 2013;178(9):1505–1512.

14. Lessler J, Reich NG, Brookmeyer R, Perl TM, Nelson KE, Cummings DAT. Incubation periods of acute respiratory viral infections: a systematic review. Lancet Infect Dis. 2009;9(5):291–300.

15. Perez A, et al. Game over for the baseline: influenza hospitalization patterns before, during, and after the COVID-19 pandemic (FluSurv-NET, 2009–2025). Infect Dis Rep. 2025. doi:10.3390/idr18030061 [VERIFY author list, volume and pages before submission]

16. Munafò MR, Nosek BA, Bishop DVM, Button KS, Chambers CD, Percie du Sert N, et al. A manifesto for reproducible science. Nat Hum Behav. 2017;1:0021.

17. Schanzer DL, Saboui M, Lee L, Domingo FR, Mersereau T. Leading indicators and the evaluation of the performance of alerts for influenza epidemics. PLoS One. 2015;10(11):e0141776. doi:10.1371/journal.pone.0141776

18. White LA, Sun M, Burnor E, Murray EL, Hoover C, Penton C, et al. A new surveillance landscape for seasonal influenza? Comparing lab-confirmed influenza hospitalizations with other syndromic and surveillance data sources for the state of California. AJE Adv. 2026;2(2):uuag019. doi:10.1093/ajeadv/uuag019

*18 references, numbered in order of first appearance, matching the convention used in the companion manuscript and the Eurosurveillance house style.*
