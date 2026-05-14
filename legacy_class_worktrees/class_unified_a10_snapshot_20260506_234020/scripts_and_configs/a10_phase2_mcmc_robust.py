import numpy as np
import subprocess
import re
import os
import glob
from scipy.interpolate import interp1d

# --- 1. 観測データの統合 (Dof=14用 計17点) ---
obs_z = np.array([0.07, 0.12, 0.2, 0.28, 0.35, 0.4, 0.48, 0.59, 0.68, 0.78, 0.88, 1.04, 1.3, 1.43, 1.53, 1.75])
obs_h = np.array([69.0, 68.6, 72.9, 88.8, 82.7, 95.0, 97.0, 104.0, 92.0, 104.5, 114.0, 148.0, 168.0, 177.0, 140.0, 202.0])
obs_err = np.array([19.6, 26.2, 29.6, 36.6, 8.4, 17.0, 62.0, 13.0, 8.0, 12.0, 20.0, 20.0, 17.0, 18.0, 14.0, 40.0])
h0_prior_val, h0_prior_err = 73.04, 1.04

C_KM_S = 299792.458
output_dir = 'output/phase2/'
os.makedirs(output_dir, exist_ok=True)
save_file = 'a10_phase2_mcmc_chain.txt'

# ファイルの初期化（ヘッダー書き込み）
with open(save_file, 'w') as f:
    f.write("# H0 k Omega_rbh chi2\n")

def get_chi2(h0, k, omega_rbh):
    root_name = f"{output_dir}p2_tmp_"
    with open('a10_test_ver2.ini', 'r') as f: content = f.read()
    
    params = {
        'H0': f'{h0:.4f}', 'rbh_coupling_k': f'{k:.4f}', 'Omega_rbh': f'{omega_rbh:.4f}',
        'omega_b': '0.02237', 'omega_cdm': '0.120', 'n_s': '0.9649', 'A_s': '2.1e-9',
        'root': root_name
    }
    for k_p, v_p in params.items():
        content = re.sub(rf'{k_p} = .*', f'{k_p} = {v_p}', content)
    
    with open('tmp_p2.ini', 'w') as f: f.write(content)
    
    # タイムアウト付きで実行 (15秒以上かかる異常積分は強制終了)
    try:
        subprocess.run(['./class', 'tmp_p2.ini'], capture_output=True, timeout=15)
    except subprocess.TimeoutExpired:
        return 1e10 # フリーズしたパラメータは棄却
    
    files = glob.glob(f"{root_name}*background.dat")
    if not files: return 1e10
    
    data = np.loadtxt(max(files, key=os.path.getctime))
    f_interp = interp1d(data[:, 0][::-1], (data[:, 3] * C_KM_S)[::-1], fill_value="extrapolate")
    
    chi2_cc = np.sum(((obs_h - f_interp(obs_z)) / obs_err)**2)
    chi2_h0 = ((h0 - h0_prior_val) / h0_prior_err)**2
    return chi2_cc + chi2_h0

# --- MCMC サンプリング (1,000ステップ) ---
n_steps = 1000
curr_p = np.array([73.0, 3.3, 0.05])
curr_chi2 = get_chi2(*curr_p)
sigmas = np.array([0.3, 0.2, 0.01])

print(f"--- Phase 2 MCMC 開始 (Sequential Save Mode) ---")
for i in range(n_steps):
    prop_p = curr_p + np.random.normal(0, sigmas)
    
    # Priorの適正化: kの上限を4.5に変更し、積分器の破綻を回避
    if not (65 < prop_p[0] < 80 and 0 < prop_p[1] < 4.5 and 0.01 < prop_p[2] < 0.2):
        prop_chi2 = 1e10
    else:
        prop_chi2 = get_chi2(*prop_p)
        
    if np.random.rand() < np.exp(-0.5 * (prop_chi2 - curr_chi2)):
        curr_p, curr_chi2 = prop_p, prop_chi2
    
    # 1ステップごとにファイルへ追記
    with open(save_file, 'a') as f:
        f.write(f"{curr_p[0]:.4f} {curr_p[1]:.4f} {curr_p[2]:.4f} {curr_chi2:.4f}\n")
        
    if i % 50 == 0: 
        print(f"Step {i}: H0={curr_p[0]:.2f}, k={curr_p[1]:.2f}, Omega_rbh={curr_p[2]:.4f}, chi2={curr_chi2:.2f}")

print("\n[Phase 2 完了] サンプリングが正常に終了しました。")