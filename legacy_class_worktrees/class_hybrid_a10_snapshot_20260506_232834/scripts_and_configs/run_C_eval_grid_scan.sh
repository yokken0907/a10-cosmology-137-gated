#!/usr/bin/env bash
set -euo pipefail

# Small diagnostic grid scan for A10 free-gate model.
# It generates 12 evaluate-only Cobaya YAMLs, runs them one by one,
# and writes a compact TSV summary.

OUTDIR="chains"
mkdir -p "$OUTDIR"
SUMMARY="$OUTDIR/run_C_eval_grid_summary.tsv"

PHI_VALUES=(136 137.47 139 142)
LOGV_VALUES=(-2 -1 0)

# Fixed cosmological / nuisance reference point from the successful evaluate pass.
H0=68.206
OMEGA_B=0.0223
OMEGA_CDM=0.1194
A_S=2.1e-9
N_S=0.965
TAU_REIO=0.055
A_PLANCK=0.9979438672394767
CALIB_100T=1.0007215437872674
CALIB_217T=0.9968033223830819
A_POL=1.0
CALIB_100P=1.021
CALIB_143P=0.966
CALIB_217P=1.04
CIB_INDEX=-1.3
A_CIB_217=47.27189754360289
XI_SZ_CIB=0.04675702062808247
A_SZ=8.84757863791849
KSZ_NORM=2.476366286151665
GAL545_A_100=9.319800029433269
GAL545_A_143=12.333491727539368
GAL545_A_143_217=22.026422454904782
GAL545_A_217=59.80846171972057
A_SBPX_100_100_TT=1.0
A_SBPX_143_143_TT=1.0
A_SBPX_143_217_TT=1.0
A_SBPX_217_217_TT=1.0
PS_A_100_100=276.2863095433778
PS_A_143_143=35.59187410732969
PS_A_143_217=48.771338238159146
PS_A_217_217=140.36394523801764
GALF_TE_INDEX=-2.4
GALF_TE_A_100=0.17216329567074776
GALF_TE_A_100_143=0.03694740350221859
GALF_TE_A_100_217=0.564368432565184
GALF_TE_A_143=0.12421921085928826
GALF_TE_A_143_217=0.6947514506576826
GALF_TE_A_217=2.0621337529747565
GALF_EE_INDEX=-2.4
GALF_EE_A_100=0.055
GALF_EE_A_100_143=0.04
GALF_EE_A_100_217=0.094
GALF_EE_A_143=0.086
GALF_EE_A_143_217=0.21
GALF_EE_A_217=0.7
A_CNOISE_E2E_100_100_EE=1.0
A_CNOISE_E2E_143_143_EE=1.0
A_CNOISE_E2E_217_217_EE=1.0
A_SBPX_100_100_EE=1.0
A_SBPX_100_143_EE=1.0
A_SBPX_100_217_EE=1.0
A_SBPX_143_143_EE=1.0
A_SBPX_143_217_EE=1.0
A_SBPX_217_217_EE=1.0

printf "prefix\tphi_trigger\tlog10_V0\tua10_V0\tloglike\tchi2_shoes\tchi2_CMB\tchi2_SN\tstatus\n" > "$SUMMARY"

run_one() {
  local phi="$1"
  local logv="$2"
  local prefix="run_C_eval_phi_${phi}_logV_${logv}"
  local yaml="$OUTDIR/${prefix}.yaml"
  local stdout_log="$OUTDIR/${prefix}.stdout.log"

  cat > "$yaml" <<YAML
output: $OUTDIR/$prefix

theory:
  classy:
    path: .
    extra_args:
      N_ncdm: 1
      N_ur: 2.0328

likelihood:
  planck_2018_highl_plik.TT:
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
  H0: $H0
  omega_b: $OMEGA_B
  omega_cdm: $OMEGA_CDM
  A_s: $A_S
  n_s: $N_S
  tau_reio: $TAU_REIO
  log10_ua10_V0: $logv
  ua10_V0:
    value: 'lambda log10_ua10_V0: 10**log10_ua10_V0'
  ua10_phi_trigger: $phi
  ua10_f_ax: 0.1
  ua10_Gamma0: 1.0
  ua10_n_ax: 2.5

  A_planck: $A_PLANCK
  calib_100T: $CALIB_100T
  calib_217T: $CALIB_217T
  A_pol: $A_POL
  calib_100P: $CALIB_100P
  calib_143P: $CALIB_143P
  calib_217P: $CALIB_217P
  cib_index: $CIB_INDEX
  A_cib_217: $A_CIB_217
  xi_sz_cib: $XI_SZ_CIB
  A_sz: $A_SZ
  ksz_norm: $KSZ_NORM
  gal545_A_100: $GAL545_A_100
  gal545_A_143: $GAL545_A_143
  gal545_A_143_217: $GAL545_A_143_217
  gal545_A_217: $GAL545_A_217
  A_sbpx_100_100_TT: $A_SBPX_100_100_TT
  A_sbpx_143_143_TT: $A_SBPX_143_143_TT
  A_sbpx_143_217_TT: $A_SBPX_143_217_TT
  A_sbpx_217_217_TT: $A_SBPX_217_217_TT
  ps_A_100_100: $PS_A_100_100
  ps_A_143_143: $PS_A_143_143
  ps_A_143_217: $PS_A_143_217
  ps_A_217_217: $PS_A_217_217
  galf_TE_index: $GALF_TE_INDEX
  galf_TE_A_100: $GALF_TE_A_100
  galf_TE_A_100_143: $GALF_TE_A_100_143
  galf_TE_A_100_217: $GALF_TE_A_100_217
  galf_TE_A_143: $GALF_TE_A_143
  galf_TE_A_143_217: $GALF_TE_A_143_217
  galf_TE_A_217: $GALF_TE_A_217
  galf_EE_index: $GALF_EE_INDEX
  galf_EE_A_100: $GALF_EE_A_100
  galf_EE_A_100_143: $GALF_EE_A_100_143
  galf_EE_A_100_217: $GALF_EE_A_100_217
  galf_EE_A_143: $GALF_EE_A_143
  galf_EE_A_143_217: $GALF_EE_A_143_217
  galf_EE_A_217: $GALF_EE_A_217
  A_cnoise_e2e_100_100_EE: $A_CNOISE_E2E_100_100_EE
  A_cnoise_e2e_143_143_EE: $A_CNOISE_E2E_143_143_EE
  A_cnoise_e2e_217_217_EE: $A_CNOISE_E2E_217_217_EE
  A_sbpx_100_100_EE: $A_SBPX_100_100_EE
  A_sbpx_100_143_EE: $A_SBPX_100_143_EE
  A_sbpx_100_217_EE: $A_SBPX_100_217_EE
  A_sbpx_143_143_EE: $A_SBPX_143_143_EE
  A_sbpx_143_217_EE: $A_SBPX_143_217_EE
  A_sbpx_217_217_EE: $A_SBPX_217_217_EE

sampler:
  evaluate: null

debug: False
stop_at_error: True
YAML

  echo "=== Running $prefix ==="
  local status="ok"
  if ! cobaya-run "$yaml" --force > "$stdout_log" 2>&1; then
    status="fail"
  fi

  local uav0="nan"
  local loglike="nan"
  local chi2shoes="nan"
  local chi2cmb="nan"
  local chi2sn="nan"

  if [[ "$status" == "ok" ]]; then
    uav0=$(grep -E '^ +[0-9]{4}-.*\[evaluate\] +ua10_V0 =' "$stdout_log" | tail -n 1 | awk -F'= ' '{print $2}' | tr -d ' ')
    loglike=$(grep -E '^ +[0-9]{4}-.*\[evaluate\] log-likelihood =' "$stdout_log" | tail -n 1 | awk -F'= ' '{print $2}' | tr -d ' ')
    chi2shoes=$(grep -E '^ +[0-9]{4}-.*\[evaluate\] +chi2_shoes_H0 =' "$stdout_log" | tail -n 1 | awk -F'= ' '{print $2}' | tr -d ' ')
    chi2cmb=$(grep -E '^ +[0-9]{4}-.*\[evaluate\] +chi2__CMB =' "$stdout_log" | tail -n 1 | awk -F'= ' '{print $2}' | tr -d ' ')
    chi2sn=$(grep -E '^ +[0-9]{4}-.*\[evaluate\] +chi2__SN =' "$stdout_log" | tail -n 1 | awk -F'= ' '{print $2}' | tr -d ' ')
  fi

  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
    "$prefix" "$phi" "$logv" "$uav0" "$loglike" "$chi2shoes" "$chi2cmb" "$chi2sn" "$status" >> "$SUMMARY"
}

for phi in "${PHI_VALUES[@]}"; do
  for logv in "${LOGV_VALUES[@]}"; do
    run_one "$phi" "$logv"
  done
done

echo
echo "Done. Summary written to: $SUMMARY"
column -ts $'\t' "$SUMMARY"
