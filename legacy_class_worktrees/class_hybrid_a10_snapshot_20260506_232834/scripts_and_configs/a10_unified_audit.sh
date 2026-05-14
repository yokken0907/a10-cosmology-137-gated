#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
OUTDIR="${2:-$ROOT/audit_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUTDIR"

log(){ printf '[audit] %s\n' "$*"; }

log "ROOT=$ROOT"
log "OUTDIR=$OUTDIR"

# 1) Source-level inventory
log "Collecting source-level inventory"
{
  echo "# has_unified_a10 occurrences"
  grep -RIn "has_unified_a10" "$ROOT/source" "$ROOT/include" || true
  echo
  echo "# ua10_V0 occurrences"
  grep -RIn "ua10_V0" "$ROOT/source" "$ROOT/include" || true
  echo
  echo "# ua10_phi_trigger occurrences"
  grep -RIn "ua10_phi_trigger" "$ROOT/source" "$ROOT/include" || true
  echo
  echo "# ua10_f_ax occurrences"
  grep -RIn "ua10_f_ax" "$ROOT/source" "$ROOT/include" || true
  echo
  echo "# ua10_Gamma0 occurrences"
  grep -RIn "ua10_Gamma0" "$ROOT/source" "$ROOT/include" || true
  echo
  echo "# ua10_n_ax occurrences"
  grep -RIn "ua10_n_ax" "$ROOT/source" "$ROOT/include" || true
} > "$OUTDIR/source_inventory.txt"

# 2) Focused extracts from source files
log "Extracting focused source windows"
for f in "$ROOT/source/input.c" "$ROOT/source/background.c" "$ROOT/source/perturbations.c" "$ROOT/include/background.h"; do
  [[ -f "$f" ]] || continue
  base=$(basename "$f")
  cp "$f" "$OUTDIR/${base}.full.txt"
  {
    echo "# Focused windows for $f"
    for pat in has_unified_a10 ua10_V0 ua10_phi_trigger ua10_f_ax ua10_Gamma0 ua10_n_ax; do
      echo
      echo "## pattern: $pat"
      grep -n "$pat" "$f" | while IFS=: read -r line _; do
        start=$(( line > 20 ? line-20 : 1 ))
        end=$(( line+30 ))
        echo "--- lines $start-$end around $pat ---"
        sed -n "${start},${end}p" "$f"
      done || true
    done
  } > "$OUTDIR/${base}.focus.txt"
done

# 3) YAML/config inventory
log "Collecting YAML inventory"
find "$ROOT" -maxdepth 2 \( -name '*.yaml' -o -name '*.yml' \) | sort > "$OUTDIR/yaml_list.txt"

log "Extracting A10-related YAML lines"
while IFS= read -r y; do
  rel=${y#"$ROOT"/}
  {
    echo "===== $rel ====="
    grep -nE 'has_unified_a10|ua10_|a10_gate|log10_ua10_V0|ua10_log10V0|non_linear|lensing|output|N_ncdm|N_ur' "$y" || true
    echo
  } >> "$OUTDIR/yaml_a10_lines.txt"
done < "$OUTDIR/yaml_list.txt"

# 4) Curated comparisons if files exist
log "Preparing curated config comparisons"
compare(){
  local a="$1"; local b="$2"; local name="$3"
  if [[ -f "$ROOT/$a" && -f "$ROOT/$b" ]]; then
    diff -u "$ROOT/$a" "$ROOT/$b" > "$OUTDIR/$name.diff" || true
  fi
}

compare "run_B_fixed137.yaml" "run_C_bestfit(1).yaml" "runB_vs_runCbestfit.diff"
compare "run_B_fixed137.input.yaml" "run_B_fixed137.updated.yaml" "runB_input_vs_updated.diff"
compare "run_C_eval_has_a10.yaml" "bridge_eval_A_scan730_best_v2.yaml" "eval_hasA10_vs_bridgeA.diff"
compare "bridge_eval_A_scan730_best_v2.yaml" "bridge_eval_C_runB_fixed137_control_v3.yaml" "bridgeA_vs_bridgeC.diff"

# 5) Chain/header inspection
log "Collecting chain headers"
find "$ROOT" -maxdepth 2 -type f \( -name '*.txt' -o -name '*.minimum*' -o -name '*.margestats' -o -name '*.progress' \) | sort > "$OUTDIR/chain_like_files.txt"
while IFS= read -r f; do
  rel=${f#"$ROOT"/}
  {
    echo "===== $rel ====="
    head -n 5 "$f" || true
    echo
  } >> "$OUTDIR/chain_headers.txt"
done < "$OUTDIR/chain_like_files.txt"

# 6) Error pattern sweep from existing logs
log "Sweeping existing logs for known failure signatures"
find "$ROOT/chains" -maxdepth 1 -type f \( -name '*.log' -o -name '*.stdout.log' -o -name '*.txt' \) 2>/dev/null | sort > "$OUTDIR/log_files.txt" || true
while IFS= read -r f; do
  rel=${f#"$ROOT"/}
  {
    echo "===== $rel ====="
    grep -nE 'Step size too small|CosmoComputationError|did not read input parameter|NameError|has_unified_a10|ua10_phi_trigge|a10_gate|log10_ua10_V0' "$f" || true
    echo
  } >> "$OUTDIR/error_sweep.txt"
done < "$OUTDIR/log_files.txt"

# 7) One-page summary builder
log "Building machine-readable summary"
{
  echo "A10 unified audit summary"
  echo "Generated: $(date -Is)"
  echo "Root: $ROOT"
  echo
  echo "Key questions"
  echo "1. Where does has_unified_a10 branch the equations?"
  echo "2. Where are ua10_V0 / ua10_phi_trigger / ua10_f_ax / ua10_Gamma0 actually used?"
  echo "3. Do legacy YAMLs differ from unified YAMLs by more than the switch?"
  echo "4. Which historic logs show parser failures vs background solver failures?"
  echo
  echo "Artifacts"
  printf '%s\n' \
    source_inventory.txt \
    input.c.focus.txt \
    background.c.focus.txt \
    perturbations.c.focus.txt \
    background.h.focus.txt \
    yaml_a10_lines.txt \
    runB_vs_runCbestfit.diff \
    runB_input_vs_updated.diff \
    eval_hasA10_vs_bridgeA.diff \
    bridgeA_vs_bridgeC.diff \
    chain_headers.txt \
    error_sweep.txt
} > "$OUTDIR/README_SUMMARY.txt"

log "Done"
log "Open: $OUTDIR/README_SUMMARY.txt"
