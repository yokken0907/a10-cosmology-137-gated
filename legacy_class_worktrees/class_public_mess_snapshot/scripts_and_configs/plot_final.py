import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')
plt.rcParams.update({'font.size': 14, 'lines.linewidth': 2.5, 'figure.facecolor': '#121212', 'axes.facecolor': '#121212'})

# 最新のファイルを取得
bg_file = max(glob.glob('output/*background.dat'), key=os.path.getmtime)
print(f"Analyzing: {bg_file}")

# 看板（ヘッダー）の正確な解析
with open(bg_file, 'r') as f:
    for line in f:
        if '1:z' in line:
            header_line = line.replace('#', '').strip()
            # 番号付きの看板をリスト化
            raw_headers = re.split(r'\s+(?=\d+:)', header_line)
            headers = [h.split(':', 1)[1].strip() for h in raw_headers if ':' in h]
            break

data = np.loadtxt(bg_file)

# カラムのインデックスを動的に取得
try:
    idx_z = headers.index('z')
    idx_rho_y = next(i for i, h in enumerate(headers) if 'rho_a10_y' in h)
    idx_rho_x = next(i for i, h in enumerate(headers) if 'rho_a10_x' in h)
    idx_om_x = next(i for i, h in enumerate(headers) if 'Omega_a10_x' in h)
    idx_win = next(i for i, h in enumerate(headers) if 'a10_window' in h)

    z = data[:, idx_z]
    # z=20000以下のデータに絞る（初期の巨大な数値による描画崩壊を回避）
    mask = (z < 20000) & (z > 0.1)
    z_plot = z[mask]
    
    rho_y = data[mask, idx_rho_y]
    rho_x = data[mask, idx_rho_x]
    omega_x = data[mask, idx_om_x]
    window = data[mask, idx_win]

    # 1. エネルギー密度のプロット（オートスケール）
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(z_plot, rho_y, label=r'$\rho_Y$ (Parent)', color='#00ffcc')
    ax.plot(z_plot, rho_x, label=r'$\rho_X$ (Daughter)', color='#ff3366')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e4, 1)
    ax.set_xlabel('Redshift z')
    ax.set_ylabel('Energy Density (CLASS units)')
    ax.set_title(f'A10 Model: Energy Transfer (Success z*={z[idx_z]})')
    ax.legend()
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('output/plot_energy_success.png')

    # 2. Omega_X のプロット
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(z_plot, omega_x, label=r'$\Omega_X$ (Impact)', color='#ffcc00')
    ax2.plot(z_plot, window * 0.05, label='Window (Scaled)', color='white', linestyle='--', alpha=0.5)
    ax2.set_xscale('log')
    ax2.set_xlim(1e4, 1)
    ax2.set_ylim(0, 0.07) # 5.1%が見える範囲に固定
    ax2.set_xlabel('Redshift z')
    ax2.set_ylabel(r'$\Omega_X$')
    ax2.set_title('A10 Model: Expansion Contribution')
    ax2.legend()
    ax2.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('output/plot_omega_success.png')

    print("--- SUCCESS: グラフを正常に書き出しました ---")
    print(f"Column Mapping: z={idx_z}, rho_y={idx_rho_y}, rho_x={idx_rho_x}, Omega_x={idx_om_x}")

except Exception as e:
    print(f"Error mapping columns: {e}")