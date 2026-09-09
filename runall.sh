#!/usr/bin/env bash
# Regenerate every result and figure in the Paper 3 manuscript from committed
# raw inputs alone: data/flux_data.csv for Hong Kong, and us/raw.json (a pinned
# Delphi Epidata pull, issues flusurv 202632 / fluview_clinical 202633) for the
# United States replication. No network access is required.
#
# Manuscript tables are still built by hand and are NOT regenerated here.
#
# Idempotent: steps whose output already exists are skipped, so a failed run
# can be restarted without repeating finished work.
#
#   ./runall.sh          normal run
#   ./runall.sh --fresh  delete all outputs first, then run everything
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/src"; RES="$ROOT/results"; FIG="$ROOT/figures"; LOG="$ROOT/results/logs"
export PYTHONPATH="$SRC:${PYTHONPATH:-}"
PY="${PYTHON:-python3}"

if [[ "${1:-}" == "--fresh" ]]; then
  echo "[runall] --fresh: clearing results/, figures/ and derived us/ outputs"
  rm -rf "$RES" "$FIG"
  rm -f "$ROOT/us/fluview_speccurve.csv" "$ROOT/us/fluview_estimates.csv" \
        "$ROOT/us/baselines.csv"   # us/raw.json is a committed input, kept
fi
mkdir -p "$RES" "$FIG" "$LOG"

# step_root <output-path-relative-to-root> <script> [args...]
#   For steps whose output does not land in results/.
step_root () {
  local out="$1"; shift
  local script="$1"; shift
  local name; name="$(basename "$script" .py)"
  if [[ -f "$ROOT/$out" ]]; then
    echo "[skip] $name  ($out present)"
    return
  fi
  echo "[run ] $name"
  ( cd "$ROOT" && "$PY" "$script" "$@" ) > "$LOG/$name.log" 2>&1 \
    || { echo "[FAIL] $name — see results/logs/$name.log"; exit 1; }
  [[ -f "$ROOT/$out" ]] || { echo "[FAIL] $name produced no $out"; exit 1; }
}

# step <output-file> <script> [args...]
step () {
  local out="$1"; shift
  local script="$1"; shift
  local name; name="$(basename "$script" .py)"
  if [[ -f "$RES/$out" ]]; then
    echo "[skip] $name  ($out present)"
    return
  fi
  echo "[run ] $name"
  ( cd "$RES" && "$PY" "$script" "$@" ) > "$LOG/$name.log" 2>&1 \
    || { echo "[FAIL] $name — see results/logs/$name.log"; exit 1; }
  [[ -f "$RES/$out" ]] || { echo "[FAIL] $name produced no $out"; exit 1; }
}

echo "=== specification curves ==="
step paper3_anchor_speccurve.csv "$SRC/paper3_anchor_speccurve.py"
step paper3_rt_speccurve.csv     "$SRC/paper3_rt_speccurve.py"
step paper3_mem_speccurve.csv    "$SRC/paper3_mem.py"
step paper3_common_subspace.csv  "$SRC/paper3_common_subspace.py"

echo "=== robustness and operational consequence ==="
step paper3_core_subset.csv      "$SRC/paper3_core_and_ops.py"

echo "=== United States replication ==="
step_root us/fluview_speccurve.csv "$SRC/fluview_speccurve.py"

echo "=== figures ==="
step paper3_fig1_speccurve.png    "$SRC/figures/paper3_fig1_v2.py"
step paper3_fig3_allchannels.png  "$SRC/figures/paper3_fig3.py"
step paper3_fig4_method_families.png "$SRC/figures/paper3_fig4.py"
step paper3_fig2_allages.png      "$SRC/figures/paper3_figS1_allages.py"
step_root figures/paper3_fig_hk_us.png "$SRC/figures/paper3_fig_hk_us.py"
mv -f "$RES"/*.png "$FIG"/ 2>/dev/null || true
mv -f "$RES"/*.pdf "$FIG"/ 2>/dev/null || true

echo "=== verification ==="
"$PY" "$ROOT/verify.py"

echo
echo "[runall] complete. results/ figures/ regenerated from data/flux_data.csv"
echo "[runall] us/ regenerated from us/raw.json"
