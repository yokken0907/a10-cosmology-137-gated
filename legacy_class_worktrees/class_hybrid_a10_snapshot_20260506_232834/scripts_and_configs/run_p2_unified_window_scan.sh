#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/class_hybrid_a10}"
cd "$ROOT"

OUTDIR="chains"
mkdir -p "$OUTDIR"
SUMMARY="$OUTDIR/p2_unified_window_scan.tsv"

# P2_legacyA73 fixed point
H0="72.999169"
OMEGA_B="0.023437102"
OMEGA_CDM="0.10867378"
A_S="2.1207673e-09"
N_S="0.99455865"
TAU_REIO="0.071083465"
UA10_F_AX="0.11552662"
UA10_GAMMA0="0.047755317"
UA10_PHI_TRIGGER="137.90903"

# Log sweep between the continuous limit and the known cliff at 1e-4
V0_VALUES=(0 1e-16 1e-15 1e-14 1e-13 1e-12 1e-11 1e-10 1e-9 1e-8 1e-7 1e-6 1e-5 1e-4)

printf "ua10_V0\tstatus\tloglike\tchi2_CMB\tchi2_SN\tchi2_shoes\terror_hint\n" > "$SUMMARY"

make_yaml() {
  local v0="$1"
  local tag="${v0//./p}"
  local yaml="p2_unified_scan_V0_${tag}.yaml"

  cat > "$yaml" <<YAML
output: ${OUTDIR}/p2_unified_scan_V0_${tag}

theory:
  classy:
    path: .
    extra_args:
      non_linear: halofit
      N_ncdm: 1
      N_ur: 2.0328
      has_unified_a10: 'yes'

likelihood:
  planck_2018_highl_plik.TTTEEE:
    path: null
    clik_file: baseline/plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik
    prior:
      SZ: 'lambda ksz_norm, A_sz: stats.norm.logpdf(ksz_norm+1.6*A_sz, loc=9.5, scale=3.0)'
  planck_2018_lowl.TT:
  planck_2018_lowl.EE:
  bao.sdss_dr12_consensus_bao:
  sn.pantheonplus:
  shoes_H0:
    external: 'lambda _self, H0: -0.5 * ((H0 - 73.04) / 1.04)**2'
    requires: [H0]

params:
  H0: ${H0}
  omega_b: ${OMEGA_B}
  omega_cdm: ${OMEGA_CDM}
  A_s: ${A_S}
  n_s: ${N_S}
  tau_reio: ${TAU_REIO}
  ua10_V0: ${v0}
  ua10_phi_trigger: ${UA10_PHI_TRIGGER}
  ua10_f_ax: ${UA10_F_AX}
  ua10_Gamma0: ${UA10_GAMMA0}
  ua10_n_ax: 2.5

  A_planck: 0.9979438672394767
  calib_100T: 1.0007215437872674
  calib_217T: 0.9968033223830819
  A_pol: 1.0
  calib_100P: 1.021
  calib_143P: 0.966
  calib_217P: 1.04
  cib_index: -1.3
  A_cib_217: 47.27189754360289
  xi_sz_cib: 0.04675702062808247
  A_sz: 8.84757863791849
  ksz_norm: 2.476366286151665
  gal545_A_100: 9.319800029433269
  gal545_A_143: 12.333491727539368
  gal545_A_143_217: 22.026422454904782
  gal545_A_217: 59.80846171972057
  A_sbpx_100_100_TT: 1.0
  A_sbpx_143_143_TT: 1.0
  A_sbpx_143_217_TT: 1.0
  A_sbpx_217_217_TT: 1.0
  ps_A_100_100: 276.2863095433778
  ps_A_143_143: 35.59187410732969
  ps_A_143_217: 48.771338238159146
  ps_A_217_217: 140.36394523801764
  galf_TE_index: -2.4
  galf_TE_A_100: 0.17216329567074776
  galf_TE_A_100_143: 0.03694740350221859
  galf_TE_A_100_217: 0.564368432565184
  galf_TE_A_143: 0.12421921085928826
  galf_TE_A_143_217: 0.6947514506576826
  galf_TE_A_217: 2.0621337529747565
  galf_EE_index: -2.4
  galf_EE_A_100: 0.055
  galf_EE_A_100_143: 0.04
  galf_EE_A_100_217: 0.094
  galf_EE_A_143: 0.086
  galf_EE_A_143_217: 0.21
  galf_EE_A_217: 0.7
  A_cnoise_e2e_100_100_EE: 1.0
  A_cnoise_e2e_143_143_EE: 1.0
  A_cnoise_e2e_217_217_EE: 1.0
  A_sbpx_100_100_EE: 1.0
  A_sbpx_100_143_EE: 1.0
  A_sbpx_100_217_EE: 1.0
  A_sbpx_143_143_EE: 1.0
  A_sbpx_143_217_EE: 1.0
  A_sbpx_217_217_EE: 1.0

sampler:
  evaluate: null

debug: False
stop_at_error: True
YAML

  echo "$yaml"
}

extract_or_nan() {
  local pat="$1"
  local file="$2"
  local value
  value=$(grep -E "$pat" "$file" | tail -n 1 | awk -F'= ' '{print $2}' | tr -d ' ' || true)
  if [[ -z "${value}" ]]; then
    echo "nan"
  else
    echo "$value"
  fi
}

for v0 in "${V0_VALUES[@]}"; do
  yaml=$(make_yaml "$v0")
  prefix="${yaml%.yaml}"
  stdout_log="${OUTDIR}/${prefix}.stdout.log"
  echo "=== Running ${yaml} ==="
  status="ok"
  if ! cobaya-run "$yaml" --force > "$stdout_log" 2>&1; then
    status="fail"
  fi
  loglike="nan"
  chi2cmb="nan"
  chi2sn="nan"
  chi2shoes="nan"
  error_hint=""
  if [[ "$status" == "ok" ]]; then
    loglike=$(extract_or_nan '\[evaluate\] log-likelihood =' "$stdout_log")
    chi2cmb=$(extract_or_nan '\[evaluate\]\s+chi2__CMB =' "$stdout_log")
    chi2sn=$(extract_or_nan '\[evaluate\]\s+chi2__SN =' "$stdout_log")
    chi2shoes=$(extract_or_nan '\[evaluate\]\s+chi2_shoes_H0 =' "$stdout_log")
  else
    error_hint=$(grep -E 'Step size too small|CosmoComputationError|CosmoSevereError' "$stdout_log" | tail -n 1 | sed 's/\t/ /g' || true)
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
    "$v0" "$status" "$loglike" "$chi2cmb" "$chi2sn" "$chi2shoes" "$error_hint" >> "$SUMMARY"
done

echo "Wrote $SUMMARY"
column -ts $'\t' "$SUMMARY"
