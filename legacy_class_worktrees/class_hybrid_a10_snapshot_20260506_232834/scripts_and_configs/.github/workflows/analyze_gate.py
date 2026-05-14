import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# 最新の2つのデータファイルを取得
files = glob.glob('output/a10_test_*_cl.dat')
files.sort(key=os.path.getmtime)
standard_file, a10_file = files[-1], files[-2] # 前回の結果との比較

# データの読み込み
data_std = np.genfromtxt(standard_file, comments='#')
data_a10 = np.genfromtxt(a10_file, comments='#')

l = data_std[:, 0]
tt_std = data_std[:, 1]
tt_a10 = data_a10[:, 1]

# 残差（ズレの比率）を計算
residual = (tt_a10 - tt_std) / tt_std * 100

# --- プロット作成 ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# 上段：生のスペクトル
ax1.plot(l, tt_std, 'k--', label='Standard LCDM', alpha=0.6)
ax1.plot(l, tt_a10, 'r-', label='Unified A10 (137 Gate)', linewidth=2)
ax1.set_yscale('log')
ax1.set_ylabel(r'$l(l+1)C_l^{TT} / 2\pi$')
ax1.set_title('Scientific Analysis of the 137 Gate effect')
ax1.legend()
ax1.grid(True, alpha=0.2)

# 下段：残差（これが真実を語る）
ax2.plot(l, residual, color='blue', linewidth=1.5)
ax2.axhline(0, color='black', linestyle='-')
ax2.set_ylabel('Difference [%]')
ax2.set_xlabel('Multipole Moment (l)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('scientific_analysis.png', dpi=300)
print(f"🔬 解析完了！ 'scientific_analysis.png' を確認してください。")