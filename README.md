# Specification curve analysis of influenza onset lead times, Hong Kong and the United States

Everything needed to reproduce, review or submit Paper 3.

**Title.** Whether a surveillance signal appears to lead laboratory positivity in
influenza onset detection is determined by analytic choice and by method family:
a specification curve analysis of thirteen channels and three estimator classes,
Hong Kong, 2014–2026

**Target.** Eurosurveillance, Research article. Within every limit: body 3,499
words (≤3,500), abstract 249 (≤250), 20 references (15–30), 3 in-text figures and
5 tables against a ≤6 illustration limit, plus 3 supplementary tables, 3
supplementary notes and 2 supplementary figures.

---

## Reproduce it

```bash
pip install -r requirements.txt
./runall.sh --fresh
```

About nine minutes, and **no network access is required**. Regenerates every
result and figure from the committed raw inputs — `data/flux_data.csv` for Hong
Kong and `us/raw.json` for the United States — then runs `verify.py`, which
checks 58 headline numbers in the manuscript against the freshly generated
results and exits nonzero if any of them drifts. Nothing in `results/`,
`figures/` or the derived files in `us/` is maintained by hand.

`./runall.sh` without `--fresh` skips steps whose output already exists, so an
interrupted run restarts without repeating finished work. `--fresh` clears
derived outputs but never `us/raw.json`, which is a committed input.

**Manuscript tables are still assembled by hand and are not regenerated here.**
That is the one part of the build that is not yet scripted.

Last full clean run: 9 September 2026, **58/58 checks passed**.

## The findings

**Baseline anchoring is the largest single driver in Hong Kong, and it has no
name in this literature.** Whether non-season weeks are identified from an
external reference series or from the channel's own low quantile moves the
estimate by 26.3 days — more than the comparator threshold at 18.9 — and
reverses the sign of the pooled result, from −14.7 days to +11.6.

**The estimate spans its own plausible range.** Across 1,728 threshold
specifications the median lead reverses sign in all 13 Hong Kong channels, with
ranges of 105 to 217 days on identical data.

**The dispersion replicates on an independent system; the driver ranking does
not.** On United States surveillance (FluSurv-NET, ILINet, clinical-lab
positivity; 333 weeks, 10 seasons, 3,024 specifications per channel) the sign
reverses in 10 of 10 channels with spreads of 70 to 91 days, and own-series
anchoring lengthens apparent leads in every channel. But the comparator is the
largest dimension there at 14.4 days and anchoring only fourth at 5.6, because
CDC attaches its published baseline to influenza-like illness while CHP attaches
its own to laboratory positivity. Which unreported choice dominates is a
property of how an agency builds its threshold; that unreported choices dominate
at all is what generalises.

**The three estimator families split two to one.** A signal leads in 14–37% of
threshold specifications and 0–6% of MEM specifications, but 73–100% of R(t)
specifications. Part of the gap is definitional and is stated as such.

**The family comparison was confounded, and the paper says so.** On its own
space MEM looked 3.1× more stable than threshold crossing. Given the same 48
shared specifications the ordering reverses — 35.0 d against 49.0 d. MEM's
advantage was a narrower specification space, which is this paper's own thesis
applied to this paper. What survives is better: MEM is the only family whose
direction never reverses, 0 of 13 against 7 and 13.

**Operational consequence:** for 0–5y admissions on core specifications, the
median gap between earliest and latest defensible onset declaration is 11.5
weeks, maximum 33. Two published estimates fall inside the curve, both siding
with the magnitude-based families.

## Layout

```
data/        flux_data.csv + PROVENANCE.md      the Hong Kong input
us/          raw.json, the pinned Delphi Epidata pull   the US input
             (fluview_speccurve.csv, baselines.csv are generated)
src/         analysis scripts + paper3_common.py
src/figures/ figure scripts
results/     generated — 4 specification curves, core subset, operational gap
figures/     generated — 3 in-text figures + 2 supplementary
manuscript/  .md source, .docx for Vijay, .pdf reading copy
docs/        pre-specified plans, scored results, reporting checklist
archive/     scripts not used by the manuscript (see archive/README.md)
verify.py    58 assertions tying the manuscript to results/ and us/
runall.sh    the driver
```

`src/paper3_common.py` holds the season boundaries, channel list, labels and the
4.94% operational threshold. It exists so this analysis runs without the PINN
codebase or PyTorch — the parent project's `seir_pinn_multisignal.py` is not a
dependency.

`us/raw.json` is a pinned Delphi Epidata pull (issues `flusurv` 202632,
`fluview_clinical` 202633, retrieved 4 September 2026). It is committed rather
than re-fetched so that the replication reproduces exactly and offline; those
series are revised, so an unpinned re-pull would be an unreported analytic choice
in a paper about unreported analytic choices.

## Specification spaces

| Family | Dimensions | Specifications |
|---|---|---|
| Threshold crossing, Hong Kong | 8 (anchoring, comparator, baseline statistic, non-season definition, pandemic-era handling, smoothing, sustained rule, season set) | 1,728 |
| Threshold crossing, United States | 8 (as above, with a rolling reference period replacing the season set) | 3,024 |
| R(t), renewal equation | 7 (SI mean, SI SD, window, prior, incidence scaling, onset rule, comparator) | 864 |
| Moving epidemic method | 7 (values per season, mean type, confidence level, consecutive weeks, periods, pandemic-era handling, comparator) | 576 |
| Equal-terms subspace | 5 shared, run identically for all three families | 48 each |

22,464 + 28,224 + 11,232 + 7,488 + 1,872 estimates.

The US arm yields 28,224 rather than 3,024 × 10 = 30,240 because a channel is not
compared against itself when it supplies the comparator, so ILINet weighted ILI
is absent under the two comparator levels built on it.

## Three bugs this build caught

Recorded because all three were silent and none would have surfaced from reading
the code.

**A stale-figure overwrite.** `paper3_figure.py` wrote both the all-ages
supplementary panel and `paper3_fig1_speccurve.png`. Run after
`paper3_fig1_v2.py`, it silently replaced the current Figure 1 with a version
built on the superseded 864-specification curve. Split into
`src/figures/paper3_figS1_allages.py`, which writes one file; the old script is
in `archive/`.

**A dependency on a superseded file.** `paper3_mem.py` and
`paper3_core_and_ops.py` read `paper3_speccurve_all.csv`, the 864-row curve that
the anchoring extension replaced. Both now read
`results/paper3_anchor_speccurve.csv`.

**A hardcoded count in a figure label.** Three figure scripts carried literal
specification counts in axis labels and captions — "864 specifications",
"576-864 per method", "Seven analytic choices" — while the curve beneath them had
doubled to 1,728 across eight dimensions. The data was always correct; the labels
were not, and `verify.py` could not see them because it checks numbers in the
manuscript and cannot read pixels. Every figure label is now derived from the
curve at draw time, and `verify.py` fails if any literal specification count
reappears in a figure source.

None of the three changed a reported number. All three would have broken
reproduction, or misrepresented it, for anyone cloning the repository. That is
the point of running `--fresh`.

## Four things needing you before submission

1. **Three references are marked `[VERIFY]`** — 15 (Perez et al.), 19 (Delphi
   Epidata API) and 20 (FluSurv-NET). For 15 the title and DOI are confirmed and
   the author list is not, because PMC and PubMed both blocked automated access.
   For 19 and 20 the preferred citation form needs checking against the source.
   Per the project's citation rule, none of these may stay unverified.
2. **Ethics exemption.** Placeholder. External clock, so start it early.
3. **Repository URL and funding statement.** Placeholders. The funding statement
   is also where the RGC grant reference gets captured.
4. **Author contributions.** Drafted in the parent manuscript's wording; confirm.

## Two things stated as approximations in the paper

Our MEM is a transparent reimplementation, not the `mem` R package. The full
method selects the epidemic period by an iterative MAP-curve procedure; we use
the weeks within ±2 of each training season's peak. The Methods say so.

Past-season ILINet national baselines are not archived by CDC and were
reconstructed from the published method. Against the two seasons with published
values the reconstruction runs about 0.4 percentage points high, most likely
because non-influenza weeks were identified from clinical rather than public
health laboratory positives. That inflates leads under the operational comparator
and makes the 14.4-day US comparator swing an upper estimate. Stated in
Limitations.

## One deliberate omission

An earlier draft reported which age group crosses earliest, putting the 12–17
year group first in 0.5% of specification-seasons. That bears on a claim in the
parent manuscript, which is with the supervisor and unpublished. The section and
its methods scaffolding were removed and Figure 1 was retargeted onto outpatient
consultations. Nothing remaining in the manuscript contradicts it. The full
reconciliation, including the mechanism, is in `docs/paper3_results.md` section
4. The supporting scripts are in `archive/`.

## The honest remaining hole

One pathogen, and two surveillance systems that are not independent of each
other's analytic conventions in the way two randomly chosen systems would be.
Magnitudes are not comparable between them, because FluSurv-NET is
catchment-based while Hong Kong admissions are territory-wide, so only dispersion
and the ranking of dimensions are compared and no cross-system comparison of
median lead is made anywhere in the paper.

ERVISS remains the interesting third system, because MEM is the operational
method in Europe and the paper's revised MEM claim would then be tested in the
system that actually runs it. It was not attempted: the European Surveillance
System is mid-migration to EpiPulse Cases, and consultation-rate denominators
differ across member states, which would put a harmonisation decision upstream of
every specification. Worth revisiting once that settles.
