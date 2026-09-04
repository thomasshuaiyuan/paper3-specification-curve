#!/usr/bin/env bash
# Regenerate every result, figure and table in the Paper 3 manuscript from
# data/flux_data.csv alone. Idempotent: steps whose output already exists are
# skipped, so a failed run can be restarted without repeating finished work.
#
#   ./runall.sh          normal run
#   ./runall.sh --fresh  delete all outputs first, then run everything
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/src"; RES="$ROOT/results"; FIG="$ROOT/figures"; LOG="$ROOT/results/logs"
export PYTHONPATH="$SRC:${PYTHONPATH:-}"
PY="${PYTHON:-python3}"

if [[ "${1:-}" == "--fresh" ]]; then
  echo "[runall] --fresh: clearing results/ and figures/"
  rm -rf "$RES" "$FIG"
fi
mkdir -p "$RES" "$FIG" "$LOG"

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

echo "=== figures ==="
step paper3_fig1_speccurve.png    "$SRC/figures/paper3_fig1_v2.py"
step paper3_fig3_allchannels.png  "$SRC/figures/paper3_fig3.py"
step paper3_fig4_method_families.png "$SRC/figures/paper3_fig4.py"
step paper3_fig2_allages.png      "$SRC/figures/paper3_figS1_allages.py"
mv -f "$RES"/*.png "$FIG"/ 2>/dev/null || true
mv -f "$RES"/*.pdf "$FIG"/ 2>/dev/null || true

echo "=== verification ==="
"$PY" "$ROOT/verify.py"

echo
echo "[runall] complete. results/ figures/ regenerated from data/flux_data.csv"
