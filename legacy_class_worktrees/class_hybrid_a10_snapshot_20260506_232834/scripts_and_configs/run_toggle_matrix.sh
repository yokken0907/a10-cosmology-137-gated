#!/usr/bin/env bash
set -euo pipefail
mkdir -p chains
printf 'case	status	loglike	chi2_CMB	chi2_SN	chi2_shoes	error_hint
' > chains/toggle_matrix_summary.tsv

run_one(){
  local yaml="$1"
  local base="${yaml%.yaml}"
  local log="chains/${base}.stdout.log"
  local status="ok"
  if ! cobaya-run "$yaml" --force > "$log" 2>&1; then status="fail"; fi
  local ll=nan c=nan s=nan h=nan err=""
  if [[ "$status" == "ok" ]]; then
    ll=$(grep -E '\[evaluate\] log-likelihood =' "$log" | tail -n 1 | awk -F'= ' '{print $2}')
    c=$(grep -E '\[evaluate\][[:space:]]+chi2__CMB =' "$log" | tail -n 1 | awk -F'= ' '{print $2}')
    s=$(grep -E '\[evaluate\][[:space:]]+chi2__SN =' "$log" | tail -n 1 | awk -F'= ' '{print $2}')
    h=$(grep -E '\[evaluate\][[:space:]]+chi2_shoes_H0 =' "$log" | tail -n 1 | awk -F'= ' '{print $2}')
  else
    err=$(grep -E 'Step size too small|CosmoComputationError|Class did not read input parameter|NameError' "$log" | tail -n 1 | sed 's/	/ /g')
  fi
  printf '%s	%s	%s	%s	%s	%s	%s
' "$base" "$status" "$ll" "$c" "$s" "$h" "$err" >> chains/toggle_matrix_summary.tsv
}

run_one toggle_P0_baseline68_off_V0_0p0.yaml
run_one toggle_P0_baseline68_on_V0_0p0.yaml
run_one toggle_P0_baseline68_off_V0_1em16.yaml
run_one toggle_P0_baseline68_on_V0_1em16.yaml
run_one toggle_P0_baseline68_off_V0_1em4.yaml
run_one toggle_P0_baseline68_on_V0_1em4.yaml
run_one toggle_P1_controlC_off_V0_0p0.yaml
run_one toggle_P1_controlC_on_V0_0p0.yaml
run_one toggle_P1_controlC_off_V0_1em16.yaml
run_one toggle_P1_controlC_on_V0_1em16.yaml
run_one toggle_P1_controlC_off_V0_1em4.yaml
run_one toggle_P1_controlC_on_V0_1em4.yaml
run_one toggle_P2_legacyA73_off_V0_0p0.yaml
run_one toggle_P2_legacyA73_on_V0_0p0.yaml
run_one toggle_P2_legacyA73_off_V0_1em16.yaml
run_one toggle_P2_legacyA73_on_V0_1em16.yaml
run_one toggle_P2_legacyA73_off_V0_1em4.yaml
run_one toggle_P2_legacyA73_on_V0_1em4.yaml

column -ts $'	' chains/toggle_matrix_summary.tsv