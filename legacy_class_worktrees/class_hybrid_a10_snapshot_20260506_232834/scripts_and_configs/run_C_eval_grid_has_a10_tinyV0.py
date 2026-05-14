import re
import subprocess
from pathlib import Path

outdir = Path('chains')
outdir.mkdir(exist_ok=True)
summary = outdir / 'run_C_eval_grid_has_a10_tinyV0_summary.tsv'
summary.write_text('prefix\tphi_trigger\tua10_V0\tloglike\tchi2_shoes\tchi2_CMB\tchi2_SN\tstatus\n', encoding='utf-8')

phi_values = [0.5, 137.47]
v0_values = [1e-8, 1e-7, 1e-6, 1e-5]

base = {
    'H0': 68.206,
    'omega_b': 0.0223,
    'omega_cdm': 0.1194,
    'A_s': 2.1e-09,
    'n_s': 0.965,
    'tau_reio': 0.055,
    'ua10_f_ax': 0.1,
    'ua10_Gamma0': 1.0,
    'ua10_n_ax': 2.5,
    'A_planck': 0.9997827805983069,
    'calib_100T': 1.0007215437872674,
    'calib_217T': 0.9968033223830819,
    'A_pol': 1.0,
    'calib_100P': 1.021,
    'calib_143P': 0.966,
    'calib_217P': 1.04,
    'cib_index': -1.3,
    'A_cib_217': 47.27189754360289,
    'xi_sz_cib': 0.04675702062808247,
    'A_sz': 8.84757863791849,
    'ksz_norm': 2.476366286151665,
    'gal545_A_100': 9.319800029433269,
    'gal545_A_143': 12.333491727539368,
    'gal545_A_143_217': 22.026422454904782,
    'gal545_A_217': 59.80846171972057,
    'A_sbpx_100_100_TT': 1.0,
    'A_sbpx_143_143_TT': 1.0,
    'A_sbpx_143_217_TT': 1.0,
    'A_sbpx_217_217_TT': 1.0,
    'ps_A_100_100': 276.2863095433778,
    'ps_A_143_143': 35.59187410732969,
    'ps_A_143_217': 48.771338238159146,
    'ps_A_217_217': 140.36394523801764,
    'galf_TE_index': -2.4,
    'galf_TE_A_100': 0.17216329567074776,
    'galf_TE_A_100_143': 0.03694740350221859,
    'galf_TE_A_100_217': 0.564368432565184,
    'galf_TE_A_143': 0.12421921085928826,
    'galf_TE_A_143_217': 0.6947514506576826,
    'galf_TE_A_217': 2.0621337529747565,
    'galf_EE_index': -2.4,
    'galf_EE_A_100': 0.055,
    'galf_EE_A_100_143': 0.04,
    'galf_EE_A_100_217': 0.094,
    'galf_EE_A_143': 0.086,
    'galf_EE_A_143_217': 0.21,
    'galf_EE_A_217': 0.7,
    'A_cnoise_e2e_100_100_EE': 1.0,
    'A_cnoise_e2e_143_143_EE': 1.0,
    'A_cnoise_e2e_217_217_EE': 1.0,
    'A_sbpx_100_100_EE': 1.0,
    'A_sbpx_100_143_EE': 1.0,
    'A_sbpx_100_217_EE': 1.0,
    'A_sbpx_143_143_EE': 1.0,
    'A_sbpx_143_217_EE': 1.0,
    'A_sbpx_217_217_EE': 1.0,
}


def extract(pattern: str, text: str, default: str = 'nan') -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else default


for phi in phi_values:
    for v0 in v0_values:
        phi_tag = str(phi).replace('-', 'm').replace('.', 'p')
        v0_tag = f'{v0:.0e}'.replace('-', 'm').replace('+', '').replace('.', 'p')
        prefix = f'run_C_hasA10_tinyV0_phi_{phi_tag}_V0_{v0_tag}'
        yaml_path = outdir / f'{prefix}.yaml'
        stdout_path = outdir / f'{prefix}.stdout.log'

        params = dict(base)
        params['ua10_phi_trigger'] = phi
        params['ua10_V0'] = v0

        lines = []
        lines += [f'output: {outdir}/{prefix}', '']
        lines += ['theory:', '  classy:', '    path: .', '    extra_args:',
                  "      has_unified_a10: 'yes'",
                  '      non_linear: halofit',
                  '      N_ncdm: 1',
                  '      N_ur: 2.0328', '']
        lines += ['likelihood:',
                  '  planck_2018_highl_plik.TTTEEE:',
                  '    path: null',
                  '    clik_file: baseline/plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik',
                  '    prior:',
                  "      SZ: 'lambda ksz_norm, A_sz: stats.norm.logpdf(ksz_norm+1.6*A_sz, loc=9.5, scale=3.0)'",
                  '  planck_2018_lowl.TT:',
                  '  planck_2018_lowl.EE:',
                  '  bao.sdss_dr12_consensus_bao:',
                  '  sn.pantheonplus:',
                  '  shoes_H0:',
                  "    external: 'lambda _self, H0: -0.5 * ((H0 - 73.04) / 1.04)**2'",
                  '    requires: [H0]', '']
        lines += ['params:']
        for k, val in params.items():
            lines.append(f'  {k}: {val!r}' if isinstance(val, str) else f'  {k}: {val}')
        lines += ['', 'sampler:', '  evaluate: null', '', 'debug: False', 'stop_at_error: True', '']
        yaml_path.write_text('\n'.join(lines), encoding='utf-8')

        print(f'=== Running {prefix} ===')
        proc = subprocess.run(
            ['cobaya-run', str(yaml_path), '--force'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        stdout_path.write_text(proc.stdout, encoding='utf-8')

        status = 'ok' if proc.returncode == 0 else 'fail'
        loglike = chi2_shoes = chi2_cmb = chi2_sn = 'nan'
        if status == 'ok':
            loglike = extract(r'\[evaluate\] log-likelihood = ([^\n]+)', proc.stdout)
            chi2_shoes = extract(r'\[evaluate\]\s+chi2_shoes_H0 = ([^\n]+)', proc.stdout)
            chi2_cmb = extract(r'\[evaluate\]\s+chi2__CMB = ([^\n]+)', proc.stdout)
            chi2_sn = extract(r'\[evaluate\]\s+chi2__SN = ([^\n]+)', proc.stdout)

        with summary.open('a', encoding='utf-8') as f:
            f.write(f'{prefix}\t{phi}\t{v0}\t{loglike}\t{chi2_shoes}\t{chi2_cmb}\t{chi2_sn}\t{status}\n')

print(f'\nDone. Summary written to: {summary}')
