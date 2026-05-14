#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
cd "$ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
BKDIR="patch_backup_zero_continuity_${STAMP}"
mkdir -p "$BKDIR"

for f in source/input.c source/background.c source/perturbations.c; do
  cp "$f" "$BKDIR/$(basename "$f").bak"
done

python3 - <<'PY'
from pathlib import Path
import re
import sys

root = Path(".")
input_c = root / "source" / "input.c"
background_c = root / "source" / "background.c"
perturbations_c = root / "source" / "perturbations.c"

# ---------- input.c ----------
txt = input_c.read_text(encoding="utf-8")

needle = "  pba->ua10_Gamma0 = 0.0;\n"
insert = "  pba->ua10_Gamma0 = 0.0;\n  pba->ua10_current_Gamma = 0.0;\n"
if "pba->ua10_current_Gamma = 0.0;" not in txt:
    if needle in txt:
        txt = txt.replace(needle, insert, 1)
    else:
        print("[patch] input.c: could not find ua10_Gamma0 init block", file=sys.stderr)
        sys.exit(1)

input_c.write_text(txt, encoding="utf-8")

# ---------- background.c ----------
txt = background_c.read_text(encoding="utf-8")

# 1) reset current_Gamma early in background_functions path, before unified contributions
anchor = "  /* interacting dark radiation */\n"
reset_block = (
    "  /* unified-A10 continuity reset: V0->0 must imply no drag */\n"
    "  if (pba->has_unified_a10 == _TRUE_) {\n"
    "    pba->ua10_current_Gamma = 0.0;\n"
    "  }\n\n"
)
if "unified-A10 continuity reset" not in txt:
    if anchor in txt:
        txt = txt.replace(anchor, reset_block + anchor, 1)
    else:
        print("[patch] background.c: could not find dark-radiation anchor", file=sys.stderr)
        sys.exit(1)

# 2) Gate the rho_phi/p_phi block by ua10_V0 > 0.0
old = "    if (pba->has_unified_a10 == _TRUE_) {"
new = "    if (pba->has_unified_a10 == _TRUE_ && pba->ua10_V0 > 0.0) {"
if old in txt and new not in txt:
    txt = txt.replace(old, new, 1)
elif new not in txt:
    print("[patch] background.c: could not patch rho_phi block", file=sys.stderr)
    sys.exit(1)

# 3) Disable A-LINE block unless V0>0, and prevent raw ua10_f_ax amplitude use there
aline_comment = "/* 2. --- YOSHIMURA A-LINE V2-PRIME REBOOT --- (H の計算の直前) */"
idx = txt.find(aline_comment)
if idx == -1:
    print("[patch] background.c: could not find A-LINE block comment", file=sys.stderr)
    sys.exit(1)

aline_if_old = "if (pba->has_unified_a10 == _TRUE_) {"
aline_if_new = "if (pba->has_unified_a10 == _TRUE_ && pba->ua10_V0 > 0.0) {"
after_idx = txt.find(aline_if_old, idx)
if after_idx == -1:
    print("[patch] background.c: could not find A-LINE if block", file=sys.stderr)
    sys.exit(1)
txt = txt[:after_idx] + txt[after_idx:].replace(aline_if_old, aline_if_new, 1)

# Replace rho_tot *= (1.0 + f_star * bump); with a V0-proportional temporary gate
rho_line_old = "    rho_tot *= (1.0 + f_star * bump);"
rho_line_new = (
    "    /* TEMP zero-amplitude continuity patch: A-LINE boost must vanish as V0->0 */\n"
    "    rho_tot *= (1.0 + pba->ua10_V0 * bump);"
)
if rho_line_old in txt and rho_line_new not in txt:
    txt = txt.replace(rho_line_old, rho_line_new, 1)
elif rho_line_new not in txt:
    print("[patch] background.c: could not patch A-LINE rho_tot rescaling", file=sys.stderr)
    sys.exit(1)

background_c.write_text(txt, encoding="utf-8")

# ---------- perturbations.c ----------
txt = perturbations_c.read_text(encoding="utf-8")

cond_old = "if (pba->has_unified_a10 == _TRUE_ && pba->has_cdm == _TRUE_ && ppt->gauge == newtonian) {"
cond_new = "if (pba->has_unified_a10 == _TRUE_ && pba->has_cdm == _TRUE_ && ppt->gauge == newtonian && pba->ua10_current_Gamma != 0.0) {"

count = txt.count(cond_old)
if count < 2 and cond_new not in txt:
    print("[patch] perturbations.c: expected >=2 unified drag conditions, found", count, file=sys.stderr)
    sys.exit(1)

txt = txt.replace(cond_old, cond_new)

perturbations_c.write_text(txt, encoding="utf-8")

print("[patch] Applied zero-continuity audit patch successfully.")
PY

echo
echo "[patch] Backups saved in: $ROOT/$BKDIR"
echo "[patch] Patched files:"
echo "  - source/input.c"
echo "  - source/background.c"
echo "  - source/perturbations.c"
echo
echo "[patch] Next step: rebuild CLASS/classy using your usual build command."
echo "[patch] After rebuild, re-run:"
echo "  ./run_toggle_matrix_v2.sh"
