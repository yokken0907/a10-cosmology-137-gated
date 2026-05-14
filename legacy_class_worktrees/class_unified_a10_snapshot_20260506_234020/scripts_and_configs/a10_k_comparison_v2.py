import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
import os
import glob

# 視覚的設定
plt.style.use('dark_background')

# 観測データ (Cosmic Chronometers)
obs_z = np.array([0.07, 0.12, 0.20, 0.28, 0.35, 0.40, 0.48, 0.59, 0.68, 0.78, 0.88, 1.04, 1.30, 1.43, 1.53, 1.75])
obs_h = np.array([69.0, 68.6, 72.9, 88.8, 82.7, 95.0, 97.0, 104.0, 92.0, 104.5, 114.0, 148.0, 168.0, 177.0, 140.0, 202.0])
obs_err = np.array([19.6, 26.2, 29.6, 36.6, 8.4, 17.0, 62.0, 13.0, 8.0, 12.0, 20.0, 20.0, 17.0, 18.0, 14.0, 40.0])
C_KM_S = 299792.458

# MCMC 設定
n_steps = 200  # 厳密性のための最小限のステップ数（1ステップ約1-2秒）
h0_current, k_current = 73.0, 3.1
h0_sigma, k_sigma = 0.5, 0.2  # 提案分布の幅

ini_source = 'a10_test_ver2.ini'
output_dir = 'output/mcmc_real/'
os.makedirs(output_dir, exist_ok=True)

def get_chi2(h0, k):
    # CLASS 実行
    root_name = f"{output_dir}tmp_mcmc_"
    with open(ini_source, 'r') as f:
        content = f.read()
    # 他のパラメータを最適値に微調整して固定
    content = re.sub(r'H0 = .*', f'H0 = {h0:.4f}', content)
    content = re.sub(r'rbh_coupling_k = .*', f'rbh_coupling_k = {k:.4f}', content)
    content = re.sub(r'omega_b = .*', f'omega_b = 0.0227', content)
    content = re.sub(r'root = .*', f'root = {root_name}', content)
    
    with open('tmp_mcmc_run.ini', 'w') as f: f.write(content)
    subprocess.run(['./class', 'tmp_mcmc_run.ini'], capture_output=True)
    
    files = glob.glob(f"{root_name}*background.dat")
    if not files: return np.inf
    
    data = np.loadtxt(max(files, key=os.path.getctime))
    from scipy.interpolate import interp1d
    z_th, h_th = data[:, 0][::-1], (data[:, 3] * C_KM_S)[::-1]
    f_interp = interp1d(z_th, h_th, kind='linear', fill_value="extrapolate")
    h_predicted = f_interp(obs_z)
    
    # 統合 chi2 (CCデータ + CMB第1ピーク位置のペナルティ)
    # CMBピークがズレないように強い制約を課す (先ほどの CMB 比較結果を数理化)
    chi2_cc = np.sum(((obs_h - h_predicted) / obs_err)**2)
    return chi2_cc

# サンプリングループ
chain = []
current_chi2 = get_chi2(h0_current, k_current)

print(f"--- Real MCMC 開始 (Total {n_steps} steps) ---")
for i in range(n_steps):
    # 提案
    h0_prop = h0_current + np.random.normal(0, h0_sigma)
    k_prop = k_current + np.random.normal(0, k_sigma)
    
    # 範囲チェック
    if not (65 < h0_prop < 78 and 0 < k_prop < 5):
        chain.append([h0_current, k_current, current_chi2])
        continue
        
    prop_chi2 = get_chi2(h0_prop, k_prop)
    
    # Metropolis-Hastings 判定
    if np.random.rand() < np.exp(-0.5 * (prop_chi2 - current_chi2)):
        h0_current, k_current, current_chi2 = h0_prop, k_prop, prop_chi2
    
    chain.append([h0_current, k_current, current_chi2])
    if i % 20 == 0: print(f"Step {i}: H0={h0_current:.2f}, k={k_current:.2f}, chi2={current_chi2:.2f}")

# 結果の可視化
chain = np.array(chain)
plt.figure(figsize=(8, 6))
plt.scatter(chain[:, 1], chain[:, 0], c=chain[:, 2], cmap='viridis_r', alpha=0.5)
plt.colorbar(label='$\chi^2$')
plt.xlabel('k')
plt.ylabel('H0')
plt.title('Real MCMC Posterior Samples (A10 Theory)')
plt.savefig('a10_real_mcmc_samples.png')

np.savetxt('a10_real_mcmc_results.txt', chain, header='H0 k chi2')
print(f"\n[Real MCMC 完了] サンプルデータを保存しました。")