# FluView replication of the Paper 3 specification curve — results

*4 September 2026. Run against `docs/fluview_replication_plan.md`, whose §4 and §5 were fixed
before any US estimate existed. All five predictions are scored below. The outcome is one the
plan's §6 did not enumerate.*

*Corrected 8 October 2026: the estimate total in §1 was wrong. See the note there.*

---

## Verdict: the phenomenon replicates, the ranking of drivers does not

**Paper 3's central claim holds on an independent surveillance system.** Onset lead estimates
reverse sign under defensible analytic choices in **10 of 10 US channels**, with within-channel
spreads of 70 to 91 days. In Hong Kong it was 13 of 13.

**Paper 3's claim about *which* choice matters most does not hold.** In Hong Kong, baseline
anchoring is the largest dimension at 26.3 days, ahead of the comparator at 18.9. In the United
States the order reverses: **comparator 14.4 days, anchoring 5.6 days**, with anchoring only fourth
of eight.

That is a more interesting result than a clean replication, and it points the manuscript at a
slightly different and better-supported claim: the instability is general, the identity of the
dominant driver is system-specific.

## 1. Data and provenance

Delphi Epidata API, retrieved 4 September 2026. **Issues pinned: `flusurv` 202632,
`fluview_clinical` 202633.** 333 weeks, 10 seasons (2016/17–2025/26), matching the plan's verified
coverage exactly.

Channels: eight FluSurv-NET age-stratified hospitalisation rates plus `rate_overall`, plus ILINet
weighted ILI — ten against Hong Kong's thirteen.

**Estimate total: 28,224, not 30,240.** The first version of this file multiplied 3,024
specifications by 10 channels. That is wrong, because a channel is never compared against itself:
when ILINet weighted ILI supplies the comparator, it cannot also be the candidate signal, so `wili`
carries 1,008 specification rows rather than 3,024. Nine channels × 3,024 plus one × 1,008 =
**28,224**, which is what `us/fluview_speccurve.csv` contains and what `verify.py` now asserts. The
error was caught by that assertion on 9 September; it never entered the manuscript.

## 2. Scoring

| | Prediction | Result | |
|---|---|---|---|
| P14 | Anchoring again the largest dimension, ahead of comparator | anchor **5.6 d**, comparator **14.4 d** | **REFUTED** |
| P15 | Own-series anchoring gives longer leads; pooled mean changes sign | own longer by **+5.6 d**, 10/10 channels; sign **does not** reverse (+1.4 → +7.1) | **PARTLY CONFIRMED** |
| P16 | Channel most affected by anchoring is the most zero-inflated (`rate_age_12t17`) | largest shift is **wILI** (12.5 d); `rate_age_12t17` second (8.3 d) | **REFUTED** |
| P17 | Median lead reverses sign in ≥7 of 10 channels | **10 of 10** | **CONFIRMED** |
| P18 | Rolling three-season reference period moves the estimate by >5 days | **0.1 d** | **REFUTED** |

Swing by dimension: comparator 14.4, non-season quantile 6.9, baseline statistic 6.2, anchoring 5.6,
sustained rule 1.8, pandemic handling 0.8, smoothing 0.7, reference period 0.1.

## 3. What each result means

**P14 — the driver ranking is system-specific.** Anchoring is real in both systems and points the
same way in both, but it is not dominant here. The reason is visible in the comparator breakdown:
mean lead is **+11.3 days** under ILINet-versus-published-baseline, **+5.3** under data-derived ILI%,
and **−3.1** under data-derived positivity. The single largest lever in the US analysis is *which
indicator the operational threshold is attached to* — and that is exactly the mismatch the plan
identified in advance, that CDC publishes a baseline for ILI% while Hong Kong publishes one for
laboratory positivity. The plan called that "itself reportable." It turns out to be the biggest
thing in the US specification space.

**P15 — direction replicates, magnitude does not.** Own-series anchoring produces longer apparent
leads in **10 of 10 channels**, which is the mechanism Paper 3 describes, operating on a different
agency's data. But the pooled mean stays positive (+1.4 → +7.1) rather than reversing, so the
sign-reversal-of-the-pooled-mean result is Hong Kong–specific. Sign reversal *within channels* is
not: that is P17, and it is 10 of 10.

**P16 — refuted as stated, and the mechanism confirmed underneath it.** The largest anchoring shift
belongs to ILINet weighted ILI, which has a zero fraction of 0.000. Zero inflation cannot be its
mechanism, so P16 fails.

But wILI is a different kind of series — a bounded percentage with a high floor, not a rate that
sits at 0.0 for most of a season. **Among the nine hospitalisation channels alone, the prediction
holds cleanly**: `rate_age_12t17` has both the highest zero fraction (0.497) and the largest
anchoring shift (8.3 d), and across those nine channels Spearman ρ = **0.733, p = 0.025**. On the
full ten, including wILI, ρ = 0.267, p = 0.455.

*This restriction to nine channels is post-hoc and is labelled as such.* What it supports is a
narrower claim than P16 made: zero inflation drives the anchoring effect **among count-based rate
channels**, and something else drives it for consultation-rate percentages. The same age group, in a
different country, under a different agency, again shows the largest zero-inflation-driven shift.

**P17 — the core claim, and it replicates strongly.** Every channel reverses sign. Spreads: 91 days
for 18–29y, 40–49y and 75+y; 84 for 30–39y and wILI; 80.5 for 5–11y; 77 for 1–4y and all-ages; 70
for <1y and 12–17y. The percentage of specifications giving a positive lead runs from 31.3% (wILI)
to 62.6% (18–29y) — so "does this channel lead positivity" has no specification-independent answer
in the US either.

**P18 — a clean negative that closes a worry.** The rolling three-season reference period moves the
pooled estimate by **0.1 days**. The plan said that if this moved things materially, the Hong Kong
specification space was incomplete and should have contained it. It does not, so the Hong Kong space
was not incomplete in that respect. This is worth reporting precisely because it was pre-registered
as a possible defect in the existing paper.

## 4. Limitation to state, not bury

**CDC does not archive past-season ILINet baselines**, so the operational comparator was
reconstructed using CDC's published method — mean wILI in non-influenza weeks over the three most
recent seasons plus two standard deviations, non-influenza weeks being two or more consecutive weeks
each accounting for under 2% of the season's positives.

Two published values exist to check against: 3.0% for 2024–25 and 3.1% for 2025–26. The
reconstruction gives **3.40 and 3.49 — systematically high by about 0.4 percentage points in both**.

The bias is consistent in direction and size, most likely because non-influenza weeks were
identified from *clinical* laboratory positives (what the API exposes) rather than *public health*
laboratory positives (what CDC uses). A too-high baseline delays the comparator crossing and
therefore **inflates apparent channel leads under the `ilinet_published` level** — which is the
level producing the longest leads and driving the comparator dimension's 14.4-day swing.

So the comparator swing is an upper estimate. The direction of the finding is unaffected, but the
magnitude should be reported with this caveat, or the analysis re-run against public health
laboratory data if a source for it can be found.

Second limitation, from the plan: FluSurv-NET is catchment-based across 13 states while Hong Kong
admissions are territory-wide, so no cross-system comparison of lead *magnitude* is made anywhere
above. Only dispersion and dimension ranking are compared.

## 5. What this does to Paper 3

**It does not weaken the paper. It changes one sentence in its thesis and strengthens the rest.**

The manuscript currently rests on anchoring being the largest single dimension at 26.3 days. That
finding stands for Hong Kong and is not contradicted — but stated as a general property it is now
known to be false, and a reviewer with US data could show it. Better to say it first.

The claim that survives, and is now supported on two independent systems, is: **whether a
surveillance channel appears to lead laboratory positivity has no specification-independent answer,
in any channel, in either system**; own-series anchoring systematically lengthens apparent leads in
23 of 23 channels across the two systems; and the dimension that dominates depends on how the
agency's operational threshold is constructed.

The Limitations item about a single surveillance system can go. It is replaced by a shorter and more
defensible one about driver ranking varying across systems.

## 6. Files

- `src/fluview_speccurve.py` — the analysis, read-only on inputs
- `us/raw.json` — pinned API pull
- `us/baselines.csv` — reconstructed baselines with the two published values for validation
- `us/fluview_speccurve.csv` — 28,224 estimates collapsed to per-specification medians
- `us/fluview_estimates.csv` — season-level estimates before collapsing (gitignored; regenerate
  with `runall.sh`)

## 7. Standing constraint, unchanged

Running this was reversible and cost an afternoon. **Restructuring the manuscript around it waits
for Vijay**, who has not yet given a view on whether Paper 3 proceeds at all. Drafting the Results
subsection is not restructuring; deciding what the paper now claims is.
