import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
import os
import glob
from scipy.interpolate import interp1d

plt.style.use('dark_background')

# MCMCから導かれた「黄金のパラメータ」
# H0 = 73.4, k = 3.35 (A10) vs H0 = 67.4, k = 0.0 (LCDM)
models = {
    'Reference (Standard LCDM)': {'H0': 67.4, 'k': 0.0, 'color': '#888888', 'ls': '--'},
    'A10 Theory (Best-fit)': {'H0': 73.4, 'k': 3.35, 'color': 'springgreen', 'ls': '-'}
}

ini_source = 'a10_test_ver2.ini'
output_dir = 'output/grand_history/'
os.makedirs(output_dir, exist_ok=True)

results = {}

print("--- A10 vs LCDM: Grand History Simulation ---")

for name, p in models.items():
    root_name = f"{output_dir}{name.replace(' ', '_')}_"
    with open(ini_source, 'r') as f:
        content = f.read()
    
    # パラメータ置換
    content = re.sub(r'H0 = .*', f'H0 = {p["H0"]}', content)
    content = re.sub(r'rbh_coupling_k = .*', f'rbh_coupling_k = {p["k"]}', content)
    content = re.sub(r'root = .*', f'root = {root_name}', content)
    
    with open('tmp_grand.ini', 'w') as f: f.write(content)
    subprocess.run(['./class', 'tmp_grand.ini'], capture_output=True)
    
    files = glob.glob(f"{root_name}*background.dat")
    if files:
        data = np.loadtxt(max(files, key=os.path.getctime))
        results[name] = {'z': data[:, 0], 'H': data[:, 3] * 299792.458}

# --- プロット生成 ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

for name, res in results.items():
    ax1.plot(res['z'], res['H'], label=name, color=models[name]['color'], 
             linestyle=models[name]['ls'], linewidth=2.5)

ax1.set_yscale('log')
ax1.set_xscale('symlog', linthresh=1)
ax1.set_ylabel('$H(z)$ [km/s/Mpc]', fontsize=14)
ax1.set_title('The A10 Universe: 13.8 Billion Year Expansion History', fontsize=16)
ax1.grid(True, which='both', linestyle='--', alpha=0.3)
ax1.legend(fontsize=12)

# 偏差（A10がどれだけLCDMを「加速」させているか）
if len(results) == 2:
    z_ax = results['A10 Theory (Best-fit)']['z']
    h_a10 = results['A10 Theory (Best-fit)']['H']
    f_lcdm = interp1d(results['Reference (Standard LCDM)']['z'], results['Reference (Standard LCDM)']['H'], fill_value="extrapolate")
    ratio = (h_a10 / f_lcdm(z_ax)) - 1.0
    ax2.plot(z_ax, ratio * 100, color='gold', linewidth=2)
    ax2.axhline(0, color='white', linestyle='-', alpha=0.5)
    ax2.set_ylabel('Deviation [%]', fontsize=12)
    ax2.set_xlabel('Redshift $z$', fontsize=14)
    ax2.set_ylim(-5, 15)
    ax2.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig('a10_grand_history_final.png')
print("最終成果物を保存しました: a10_grand_history_final.png")