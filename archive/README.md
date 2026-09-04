# Archive — not part of the manuscript build

These scripts are retained as a record of work done and are **not** run by
`runall.sh`. None of their outputs appears in the manuscript.

- `paper3_figure.py` — the original two-panel Figure 1 plus the all-ages panel,
  built on the superseded 864-specification curve. It also wrote
  `paper3_fig1_speccurve.png`, so running it after `paper3_fig1_v2.py` silently
  replaced the current Figure 1 with a stale one. Replaced by
  `src/figures/paper3_fig1_v2.py` and `src/figures/paper3_figS1_allages.py`.
- `paper3_inference.py` — permutation inference for the dominance analysis
  (which age group crosses earliest). That section was removed from the
  manuscript in August 2026; see `docs/paper3_results.md` section 4.
- `paper3_age_ranking.py` — the age-ranking sensitivity analysis behind the same
  removed section.

Paths in these files are not maintained and may not resolve.
