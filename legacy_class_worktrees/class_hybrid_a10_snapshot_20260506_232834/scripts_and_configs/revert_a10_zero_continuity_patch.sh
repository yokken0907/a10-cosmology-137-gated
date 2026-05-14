#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
cd "$ROOT"

LATEST="$(ls -dt patch_backup_zero_continuity_* 2>/dev/null | head -n 1 || true)"
if [[ -z "$LATEST" ]]; then
  echo "[revert] No patch backup directory found."
  exit 1
fi

cp "$LATEST/input.c.bak" source/input.c
cp "$LATEST/background.c.bak" source/background.c
cp "$LATEST/perturbations.c.bak" source/perturbations.c

echo "[revert] Restored from $LATEST"
