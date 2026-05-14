import matplotlib.pyplot as plt
import numpy as np
import os

# ファイルの存在確認
files = ["std_00_cl.dat", "yoshi_00_cl.dat", "yoshi_a2_cl.dat"]
for f in files:
    if not os.path.exists(f):
        print(f"エラー: {f} が見つかりません。")

# データの読み込み
std = np.loadtxt("std_00_cl.dat")
yoshi_a1 = np.loadtxt("yoshi_00_cl.dat")
yoshi_a2 = np.loadtxt("yoshi_a2_cl.dat")

plt.figure(figsize=(10, 6))

# 標準モデル (グレーの点線)
plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM", alpha=0.5)
# 前回の A1 モデル (赤の点線)
plt.plot(yoshi_a1[:,0], yoshi_a1[:,1], 'r:', label="Yoshimura A1 (First Try)")
# 今回の A2 モデル (青の実線)
plt.plot(yoshi_a2[:,0], yoshi_a2[:,1], 'b-', label="Yoshimura A2 (Improved)", linewidth=2)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura Model Evolution: A1 to A2")
plt.legend()
plt.grid(True, alpha=0.2)
plt.xlim(2, 2500)

plt.savefig("evolution_result.png")
print("\n【大成功】 比較図 'evolution_result.png' を作成しました！")
