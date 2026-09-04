# Specification curve analysis of influenza onset lead times, Hong Kong 2014–2026

Everything needed to reproduce, review or submit Paper 3.

**Title.** Whether a surveillance signal appears to lead laboratory positivity in
influenza onset detection is determined by analytic choice and by method family:
a specification curve analysis of thirteen channels and three estimator classes,
Hong Kong, 2014–2026

**Target.** Eurosurveillance, Research article. Within every limit: body 3,499
words (≤3,500), abstract 250 (≤250), 18 references (15–30), 4 figures and 4
tables against a ≤6 illustration limit, plus 4 supplementary items.

---

## Reproduce it

```bash
pip install -r requirements.txt
./runall.sh --fresh
```

About nine minutes. Regenerates every result, figure and table from
`data/flux_data.csv` alone, then runs `verify.py`, which checks all 42 headline
numbers in the manuscript against the freshly generated results and **exits
nonzero if any of them drifts**. Nothing in `results/` or `figures/` is
maintained by hand.

`./runall.sh` without `--fresh` skips steps whose output already exists, so an
interrupted run restarts without repeating finished work.

Last full clean run: 4 September 2026, **42/42 checks passed**.

---

## The findings

1. **Baseline anchoring is the largest single driver, and it has no name in this
   literature.** Whether non-season weeks are identified from an external
   reference series or from the channel's own low quantile moves the estimate by
   **26.3 days** — more than the comparator threshold at 18.9 — and reverses the
   sign of the pooled result, from −14.7 days to +11.6.
2. **The estimate spans its own plausible range.** Across 1,728 threshold
   specifications the median lead reverses sign in **all 13 channels**, with
   ranges of 105 to 217 days on identical data.
3. **The three estimator families split two to one.** A signal leads in 14–37%
   of threshold specifications and 0–6% of MEM specifications, but 73–100% of
   R(t) specifications. Part of the gap is definitional and is stated as such.
4. **The family comparison was confounded, and the paper says so.** On its own
   space MEM looked 3.1× more stable than threshold crossing. Given the same 48
   shared specifications the ordering reverses — 35.0 d against 49.0 d. MEM's
   advantage was a narrower specification space, which is this paper's own thesis
   applied to this paper. What survives is better: MEM is the only family whose
   direction never reverses, 0 of 13 against 7 and 13.

Operational consequence: for 0–5y admissions on core specifications, the median
gap between earliest and latest defensible onset declaration is **11.5 weeks**,
maximum 33. Two published estimates fall inside the curve, both siding with the
magnitude-based families.

---

## Layout

```
data/        flux_data.csv + PROVENANCE.md      the only input
src/         analysis scripts + paper3_common.py
src/figures/ figure scripts
results/     generated — 4 specification curves, core subset, operational gap
figures/     generated — 3 in-text figures + 1 supplementary
manuscript/  .md source, .docx for Vijay, .pdf reading copy
docs/        pre-specified plans, scored results, reporting checklist
archive/     scripts not used by the manuscript (see archive/README.md)
verify.py    42 assertions tying the manuscript to results/
runall.sh    the driver
```

`src/paper3_common.py` holds the season boundaries, channel list, labels and the
4.94% operational threshold. It exists so this analysis runs **without the PINN
codebase or PyTorch** — the parent project's `seir_pinn_multisignal.py` is not a
dependency.

## Specification spaces

| Family | Dimensions | Specifications |
|---|---|---|
| Threshold crossing | 8 (anchoring, comparator, baseline statistic, non-season definition, pandemic-era handling, smoothing, sustained rule, season set) | 1,728 |
| R(t), renewal equation | 7 (SI mean, SI SD, window, prior, incidence scaling, onset rule, comparator) | 864 |
| Moving epidemic method | 7 (values per season, mean type, confidence level, consecutive weeks, periods, pandemic-era handling, comparator) | 576 |
| Equal-terms subspace | 5 shared, run identically for all three families | 48 each |

22,464 + 11,232 + 7,488 + 1,872 estimates.

---

## Two bugs this build caught

Recorded because both were silent and neither would have surfaced from reading
the code.

**A stale-figure overwrite.** `paper3_figure.py` wrote *both* the all-ages
supplementary panel and `paper3_fig1_speccurve.png`. Run after
`paper3_fig1_v2.py`, it silently replaced the current Figure 1 with a version
built on the superseded 864-specification curve. Split into
`src/figures/paper3_figS1_allages.py`, which writes one file; the old script is
in `archive/`.

**A dependency on a superseded file.** `paper3_mem.py` and
`paper3_core_and_ops.py` read `paper3_speccurve_all.csv`, the 864-row curve that
the anchoring extension replaced. Both now read
`results/paper3_anchor_speccurve.csv`.

Neither changed a reported number. Both would have broken reproduction for
anyone cloning the repository, which is the point of running `--fresh`.

---

## Four things needing you before submission

1. **Reference 18 (Perez et al.)** is marked `[VERIFY]`. Title and DOI are
   confirmed; the author list is not, because PMC and PubMed both blocked
   automated access. Verify or cut — cutting leaves 17, still in range.
2. **Ethics exemption.** Placeholder. External clock, so start it early.
3. **Repository URL and funding statement.** Placeholders.
4. **Author contributions.** Drafted in the parent manuscript's wording; confirm.

## Two things stated as approximations in the paper

- Our MEM is a transparent reimplementation, not the `mem` R package. The full
  method selects the epidemic period by an iterative MAP-curve procedure; we use
  the weeks within ±2 of each training season's peak. The Methods say so.
- Pandemic-era handling is inert for MEM in this season set, because no analysed
  season begins between 2020 and 2022, so the training set never changes.
  Reported as a property of the season set, not of the method.

## One deliberate omission

An earlier draft reported which age group crosses earliest, putting the 12–17
year group first in 0.5% of specification-seasons. That bears on a claim in the
parent manuscript, which is with the supervisor and unpublished. **The section
and its methods scaffolding were removed and Figure 1 was retargeted onto
outpatient consultations.** Nothing remaining in the manuscript contradicts it.
The full reconciliation, including the mechanism, is in
`docs/paper3_results.md` section 4. The supporting scripts are in `archive/`.

## The honest remaining hole

One surveillance system, one pathogen. Replication on FluView or ERVISS would
answer the obvious reviewer question. FluView is scoped and viable — CDC's
FluSurv-NET, clinical-lab positivity and ILINet are all reachable, 10 usable
seasons — and estimated at one to two days behind a pre-specified plan. The
Limitations section states the gap rather than hiding it.
