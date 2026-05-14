import matplotlib.pyplot as plt
import numpy as np

# 1. データの読み込み (CLASSの出力ファイル名に合わせてください)
file_path = 'output/a10_test_background.dat'

# ヘッダーを探して列番号を特定するか、手動で指定します
# 通常 CLASS の background 出力は 1列目が z (または tau) です
data = np.loadtxt(file_path)

# カラムのインデックスは background.h で定義した順番に依存します
# 以前の修正に基づくと、末尾の方に追加されているはずです
# (例: -3: rho_phi, -2: w_phi, -1: Gamma_drag)
z = data[:, 0]
rho_phi = data[:, -3]
w_phi = data[:, -2]
gamma_drag = data[:, -1]

# スカラー場の値 phi も読み込む必要があります（もし出力に含めていれば）
# ここでは一旦、ドラッグの挙動を確認します

fig, ax1 = plt.subplots(figsize=(10, 6))

# 左軸: エネルギー密度の進化
ax1.set_xlabel('Redshift z')
ax1.set_ylabel('Energy Density rho_phi', color='tab:blue')
ax1.loglog(z, rho_phi, label='rho_phi', color='tab:blue', lw=2)
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.invert_xaxis() # zを大きい方から表示

# 右軸: 137ゲート (Gamma_drag)
ax2 = ax1.twinx()
ax2.set_ylabel('Gamma Drag (The 137 Gate)', color='tab:red')
ax2.semilogx(z, gamma_drag, label='Gamma_drag', color='tab:red', ls='--')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Verification of Unified A10: Background Evolution')
fig.tight_layout()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.savefig('verify_a10_stage1.png')
plt.show()

print("検証用グラフを出力しました。'Gamma_drag' に鋭いピークが見えますか？")