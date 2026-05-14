#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
cd "$ROOT"

echo "[info] repaired_unified_highH0_narrow_rerun"
echo "[info] output prefix: chains/repaired_unified_highH0_narrow_rerun"

if [[ -n "${VIRTUAL_ENV:-}" ]]; then
  echo "[info] active venv: $VIRTUAL_ENV"
else
  echo "[warn] no virtualenv active"
fi

if command -v mpirun >/dev/null 2>&1; then
  mpirun -n 3 cobaya-run repaired_unified_highH0_narrow_rerun.yaml --resume
else
  cobaya-run repaired_unified_highH0_narrow_rerun.yaml --resume
fi
