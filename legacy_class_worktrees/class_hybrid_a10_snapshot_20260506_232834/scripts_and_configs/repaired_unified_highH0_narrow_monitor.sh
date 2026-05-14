#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
cd "$ROOT"

echo "[monitor] Latest files:"
ls -ltr chains/repaired_unified_highH0_narrow* 2>/dev/null || true

echo
echo "[monitor] Active cobaya/classy processes:"
ps -eo pid,etime,pcpu,pmem,cmd | grep -E 'repaired_unified_highH0_narrow|cobaya-run|python' | grep -v grep || true

echo
echo "[monitor] Tail of progress/log-like text files:"
tail -n 20 chains/repaired_unified_highH0_narrow.progress 2>/dev/null || true
tail -n 5 chains/repaired_unified_highH0_narrow.1.txt 2>/dev/null || true
