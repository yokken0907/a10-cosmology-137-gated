#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
cd "$ROOT"

echo "[info] Using repaired-unified narrow high-H0 posterior run"
echo "[info] Output prefix: chains/repaired_unified_highH0_narrow"
echo "[info] Recommend running inside the venv that successfully rebuilt classy."

if [[ -n "${VIRTUAL_ENV:-}" ]]; then
  echo "[info] Active venv: $VIRTUAL_ENV"
else
  echo "[warn] No virtualenv active."
fi

if command -v mpirun >/dev/null 2>&1; then
  echo "[info] Starting with MPI x 3"
  mpirun -n 3 cobaya-run repaired_unified_highH0_narrow.yaml --resume
else
  echo "[info] Starting single-process"
  cobaya-run repaired_unified_highH0_narrow.yaml --resume
fi
