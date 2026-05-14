#!/usr/bin/env bash
set -euo pipefail
for f in bridge_eval_A_scan730_best_v2.yaml bridge_eval_B_scan730v2_best_v2.yaml bridge_eval_C_runB_fixed137_control_v2.yaml; do
  echo "=== Running $f ==="
  cobaya-run "$f" --force | tee "chains/${f%.yaml}.stdout.log"
  echo
  grep -E '\[evaluate\] log-likelihood =|\[evaluate\]    chi2_shoes_H0 =|\[evaluate\]    chi2__CMB =|\[evaluate\]    chi2__SN =' "chains/${f%.yaml}.stdout.log" || true
  echo
 done
