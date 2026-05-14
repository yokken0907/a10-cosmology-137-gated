#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
OUTDIR="${2:-$ROOT/unified_switch_audit_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUTDIR"

SRC_BG="$ROOT/source/background.c"
SRC_PT="$ROOT/source/perturbations.c"
SRC_IN="$ROOT/source/input.c"
HDR_BG="$ROOT/include/background.h"

for f in "$SRC_BG" "$SRC_PT" "$SRC_IN" "$HDR_BG"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing required file: $f" >&2
    exit 1
  fi
done

# 1) Inventory of unified-switch references
{
  echo "# has_unified_a10 references"
  grep -n "has_unified_a10" "$SRC_BG" || true
  grep -n "has_unified_a10" "$SRC_PT" || true
  grep -n "has_unified_a10" "$SRC_IN" || true
  grep -n "has_unified_a10" "$HDR_BG" || true
} > "$OUTDIR/has_unified_a10_inventory.txt"

# 2) Inventory of ua10 parameter references
{
  echo "# ua10_V0 references"
  grep -n "ua10_V0" "$SRC_BG" || true
  grep -n "ua10_V0" "$SRC_PT" || true
  grep -n "ua10_V0" "$SRC_IN" || true
  grep -n "ua10_V0" "$HDR_BG" || true
  echo
  echo "# ua10_phi_trigger references"
  grep -n "ua10_phi_trigger" "$SRC_BG" || true
  grep -n "ua10_phi_trigger" "$SRC_PT" || true
  grep -n "ua10_phi_trigger" "$SRC_IN" || true
  grep -n "ua10_phi_trigger" "$HDR_BG" || true
  echo
  echo "# ua10_f_ax references"
  grep -n "ua10_f_ax" "$SRC_BG" || true
  grep -n "ua10_f_ax" "$SRC_PT" || true
  grep -n "ua10_f_ax" "$SRC_IN" || true
  grep -n "ua10_f_ax" "$HDR_BG" || true
  echo
  echo "# ua10_Gamma0 references"
  grep -n "ua10_Gamma0" "$SRC_BG" || true
  grep -n "ua10_Gamma0" "$SRC_PT" || true
  grep -n "ua10_Gamma0" "$SRC_IN" || true
  grep -n "ua10_Gamma0" "$HDR_BG" || true
} > "$OUTDIR/ua10_parameter_inventory.txt"

# 3) Extract focused windows around each unified switch in background.c and perturbations.c
python3 - "$SRC_BG" "$SRC_PT" "$OUTDIR" <<'PY'
from pathlib import Path
import sys

src_bg = Path(sys.argv[1])
src_pt = Path(sys.argv[2])
outdir = Path(sys.argv[3])


def extract_windows(src: Path, tag: str):
    lines = src.read_text(encoding='utf-8', errors='replace').splitlines()
    hits = [i for i, line in enumerate(lines, start=1) if 'has_unified_a10' in line]
    out = []
    for idx, lineno in enumerate(hits, start=1):
        start = max(1, lineno - 20)
        end = min(len(lines), lineno + 35)
        out.append(f"===== {tag} hit {idx}: lines {start}-{end} (anchor {lineno}) =====")
        for n in range(start, end + 1):
            out.append(f"{n:6d}: {lines[n-1]}")
        out.append("")
    (outdir / f"{tag}.focused_windows.txt").write_text("\n".join(out), encoding='utf-8')

extract_windows(src_bg, 'background')
extract_windows(src_pt, 'perturbations')
PY

# 4) Heuristic classifier: lines inside unified windows that mention ua10_V0 vs those that do not
python3 - "$OUTDIR/background.focused_windows.txt" "$OUTDIR/perturbations.focused_windows.txt" "$OUTDIR" <<'PY'
from pathlib import Path
import sys
import re

bg = Path(sys.argv[1])
pt = Path(sys.argv[2])
outdir = Path(sys.argv[3])

interesting_tokens = ['ua10_', 'rho', 'p=', ' p ', 'pressure', 'dV', 'V ', 'V=', 'Gamma', 'phi', 'source', 'friction', 'w_']

for src, name in [(bg, 'background'), (pt, 'perturbations')]:
    text = src.read_text(encoding='utf-8', errors='replace').splitlines()
    with_v0 = []
    without_v0 = []
    for line in text:
        if re.match(r'^\s*\d+:', line):
            lower = line.lower()
            if any(tok.lower() in lower for tok in interesting_tokens):
                if 'ua10_v0' in lower:
                    with_v0.append(line)
                else:
                    without_v0.append(line)
    (outdir / f"{name}.with_ua10_V0.txt").write_text("\n".join(with_v0), encoding='utf-8')
    (outdir / f"{name}.without_ua10_V0.txt").write_text("\n".join(without_v0), encoding='utf-8')
PY

# 5) Extract parser/default blocks from input.c
python3 - "$SRC_IN" "$OUTDIR" <<'PY'
from pathlib import Path
import sys

src = Path(sys.argv[1])
outdir = Path(sys.argv[2])
lines = src.read_text(encoding='utf-8', errors='replace').splitlines()
keys = ['has_unified_a10', 'ua10_V0', 'ua10_phi_trigger', 'ua10_f_ax', 'ua10_Gamma0', 'ua10_n_ax']
out = []
for key in keys:
    hits = [i for i, line in enumerate(lines, start=1) if key in line]
    out.append(f"===== {key} =====")
    for lineno in hits:
        start = max(1, lineno - 6)
        end = min(len(lines), lineno + 8)
        out.append(f"--- lines {start}-{end} around {lineno} ---")
        for n in range(start, end + 1):
            out.append(f"{n:6d}: {lines[n-1]}")
        out.append("")
(outdir / 'input_parser_defaults_focus.txt').write_text("\n".join(out), encoding='utf-8')
PY

# 6) Targeted diff prompts to run manually if needed
cat > "$OUTDIR/NEXT_COMMANDS.txt" <<'EOF2'
# Open these first:
less background.focused_windows.txt
less background.without_ua10_V0.txt
less input_parser_defaults_focus.txt

# Fast searches:
grep -n "has_unified_a10" source/background.c source/perturbations.c source/input.c include/background.h
grep -n "ua10_V0" source/background.c source/perturbations.c source/input.c include/background.h
grep -n "ua10_phi_trigger" source/background.c source/perturbations.c source/input.c include/background.h

# If you want to inspect only branches that may survive at ua10_V0=0:
grep -n -C 4 "has_unified_a10" source/background.c | grep -v "ua10_V0"
grep -n -C 4 "has_unified_a10" source/perturbations.c | grep -v "ua10_V0"
EOF2

# 7) Human-readable summary header
cat > "$OUTDIR/README_SUMMARY.txt" <<'EOF3'
Goal:
  Determine whether has_unified_a10 activates non-vanishing dynamics even when ua10_V0 = 0.

Read in this order:
  1) input_parser_defaults_focus.txt
  2) background.focused_windows.txt
  3) background.without_ua10_V0.txt
  4) perturbations.focused_windows.txt
  5) perturbations.without_ua10_V0.txt

What to flag:
  - any term inside a has_unified_a10 branch that does not multiply ua10_V0
  - any background or perturbation source added solely by has_unified_a10
  - any initial-condition change triggered by has_unified_a10 regardless of ua10_V0

Interpretation:
  - If such terms exist, unified is not a zero-amplitude limit of legacy A10.
  - If no such terms exist, investigate normalization, units, or solver stiffness next.
EOF3

echo "[inspect] ROOT=$ROOT"
echo "[inspect] OUTDIR=$OUTDIR"
echo "[inspect] Open $OUTDIR/README_SUMMARY.txt"
