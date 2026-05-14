import glob
import os
import pandas as pd
import matplotlib.pyplot as plt

# 最新のバックグラウンドデータを取得
file_list = glob.glob('output/*_background.dat')
if not file_list:
    print("データファイルが見つかりません。")
    exit()

latest_file = max(file_list, key=os.path.getctime)
print(f"読み込みファイル: {latest_file}")

# データの読み込み
df = pd.read_csv(latest_file, sep=r'\s+', comment='#', header=None)

# 必要な列名の定義（CLASSの出力順に準拠）
col_names = ['z', 'time', 'conf_time', 'H', 'comov_dist', 'ang_diam_dist', 'lum_dist', 'rs', 
             'rho_g', 'rho_b', 'rho_cdm', 'rho_lambda', 'rho_ur', 'rho_crit', 'rho_tot', 
             'p_tot', 'p_tot_prime', 'Omega_r', 'Omega_m', 'gr_D', 'gr_f', 'chi', 'u_chi', 'rho_Y', 'rho_X']
df.columns = col_names[:len(df.columns)]

# プロットの作成
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# chiの推移
ax1.plot(df['z'], df['chi'], label='chi', color='blue')
ax1.set_ylabel('Scalar Field (chi)')
ax1.legend()
ax1.grid(True)

# rho_Yとrho_Xの推移
ax2.plot(df['z'], df['rho_Y'], label='rho_Y', color='red')
ax2.plot(df['z'], df['rho_X'], label='rho_X', color='green')
ax2.set_xlabel('Redshift (z)')
ax2.set_ylabel('Energy Density')
# 極端なスケール変動や微小な計算誤差を許容するためsymlogを使用
ax2.set_yscale('symlog', linthresh=1e-10)
ax2.legend()
ax2.grid(True)

# 時間発展（zが大きい初期宇宙から小さい現在へ）に合わせてx軸を反転・対数表示
ax1.set_xscale('log')
ax2.set_xscale('log')
ax1.invert_xaxis() 

plt.tight_layout()
plt.savefig('yoshimura_theory_plot.png')
print("プロットを yoshimura_theory_plot.png として保存しました。")