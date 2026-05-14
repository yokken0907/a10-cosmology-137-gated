import numpy as np
import subprocess
import re
import os
import glob
from scipy.interpolate import interp1d

# --- 1. 観測データの定義 (CC 16点 + SH0ES 1点) ---
obs_z = np.array([0.07, 0.12, 0.2, 0.28, 0.35, 0.4, 0.48, 0.59, 0.68, 0.78, 0.88, 1.04, 1.3, 1.43, 1.53, 1.75])
obs_h = np.array([69.0, 68.6, 72.9, 88.8, 82.7, 95.0, 97.0, 104.0, 92.0, 104.5, 114.0, 148.0, 168.0, 177.0, 140.0, 202.0])
obs_err = np.array([19.6, 26.2, 29.6, 36.6, 8.4, 17.0, 62.0, 13.0, 8.0, 12.0, 20.0, 20.0, 17.0, 18.0, 14.0, 40.0])
h0_prior_val, h0_prior_err = 73.04, 1.04
n_data = len(obs_z) + 1 # 17点

C_KM_S = 299792.458
output_dir = 'output/phase2/'
os.makedirs(output_dir, exist_ok=True)

print("=== Mission 1: Standard LCDM Baseline Evaluation ===")

def get_lcdm_chi2(h0):
    root_name = f"{output_dir}lcdm_base_"
    with open('a10_test_ver2.ini', 'r') as f: content = f.read()
    
    # LCDM仕様 (k=0, Omega_rbh=0) に固定
    params = {
        'H0': f'{h0:.4f}', 'rbh_coupling_k': '0.0', 'Omega_rbh': '0.0',
        'omega_b': '0.02237', 'omega_cdm': '0.120', 'n_s': '0.9649', 'A_s': '2.1e-9',
        'root': root_name
    }
    for k_p, v_p in params.items():
        content = re.sub(rf'{k_p} = .*', f'{k_p} = {v_p}', content)
    
    with open('tmp_lcdm.ini', 'w') as f: f.write(content)
    subprocess.run(['./class', 'tmp_lcdm.ini'], capture_output=True)
    
    files = glob.glob(f"{root_name}*background.dat")
    if not files: return 1e10
    
    data = np.loadtxt(max(files, key=os.path.getctime))
    f_interp = interp1d(data[:, 0][::-1], (data[:, 3] * C_KM_S)[::-1], fill_value="extrapolate")
    
    chi2_cc = np.sum(((obs_h - f_interp(obs_z)) / obs_err)**2)
    chi2_h0 = ((h0 - h0_prior_val) / h0_prior_err)**2
    return chi2_cc + chi2_h0

# LCDMのベストフィットH0を簡易探索 (1次元)
h0_scan = np.linspace(67.0, 74.0, 50)
chi2_lcdm_list = [get_lcdm_chi2(h) for h in h0_scan]
best_idx_lcdm = np.argmin(chi2_lcdm_list)
best_h0_lcdm = h0_scan[best_idx_lcdm]
min_chi2_lcdm = chi2_lcdm_list[best_idx_lcdm]

# LCDM (パラメータ1個: H0)
aic_lcdm = min_chi2_lcdm + 2 * 1
bic_lcdm = min_chi2_lcdm + 1 * np.log(n_data)

print(f"LCDM Best-fit: H0 = {best_h0_lcdm:.2f}")
print(f"LCDM chi2 = {min_chi2_lcdm:.2f} (Dof={n_data - 1})")
print(f"LCDM AIC  = {aic_lcdm:.2f}")
print(f"LCDM BIC  = {bic_lcdm:.2f}\n")


print("=== Mission 2: A10 Model Rigorous Posterior Statistics ===")
try:
    chain = np.loadtxt('a10_phase2_mcmc_chain.txt')
    burnin = int(len(chain) * 0.2)
    clean_chain = chain[burnin:]
    
    h0_s = clean_chain[:, 0]
    k_s = clean_chain[:, 1]
    omega_s = clean_chain[:, 2]
    chi2_s = clean_chain[:, 3]
    
    # A10 Best-fit
    b_idx = np.argmin(chi2_s)
    min_chi2_a10 = chi2_s[b_idx]
    
    # A10 (パラメータ3個: H0, k, Omega_rbh)
    aic_a10 = min_chi2_a10 + 2 * 3
    bic_a10 = min_chi2_a10 + 3 * np.log(n_data)
    
    print(f"[Model Comparison]")
    print(f"A10 chi2 = {min_chi2_a10:.2f} (Dof={n_data - 3})")
    print(f"A10 AIC  = {aic_a10:.2f} (Delta AIC = {aic_a10 - aic_lcdm:.2f})")
    print(f"A10 BIC  = {bic_a10:.2f} (Delta BIC = {bic_a10 - bic_lcdm:.2f})\n")
    
    print(f"[A10 Parameters: Marginalized Posterior vs Best-fit]")
    for name, samples, best in zip(['H0', 'k', 'Omega_rbh'], [h0_s, k_s, omega_s], [h0_s[b_idx], k_s[b_idx], omega_s[b_idx]]):
        mean_v = np.mean(samples)
        median_v = np.median(samples)
        lower_1sig = np.percentile(samples, 16)
        upper_1sig = np.percentile(samples, 84)
        print(f"--- {name} ---")
        print(f"  Best-fit : {best:.4f}")
        print(f"  Mean     : {mean_v:.4f}")
        print(f"  Median   : {median_v:.4f}")
        print(f"  68% CI   : [{lower_1sig:.4f}, {upper_1sig:.4f}]")

except FileNotFoundError:
    print("MCMC chain file not found.")