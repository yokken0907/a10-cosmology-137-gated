import matplotlib.pyplot as plt
import numpy as np
import os

# ファイルの確認（A5が00番か01番か注意してください）
std_file = "std_00_cl.dat"
yoshi_a5_file = "yoshi_a5_00_cl.dat"

if not os.path.exists(yoshi_a5_file):
    # もし00がなければ01を探す
    yoshi_a5_file = "yoshi_a5_01_cl.dat"

print(f"Comparing {std_file} and {yoshi_a5_file}...")

# データの読み込み
std = np.loadtxt(std_file)
a5 = np.loadtxt(yoshi_a5_file)

plt.figure(figsize=(12, 7))

# 標準モデル（漆黒の点線）
plt.plot(std[:,0], std[:,1], color='black', linestyle='--', label="Standard LCDM ($H_0=67.4$)", alpha=0.6)

# 吉村モデル A5（鮮やかな赤の実線）
plt.plot(a5[:,0], a5[:,1], color='crimson', label="Yoshimura A5 ($H_0=72.0$)", linewidth=2.5)

plt.xlabel(r"Multipole $\ell$", fontsize=13)
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$", fontsize=13)
plt.title("The Solution to Hubble Tension: Yoshimura Model A5", fontsize=15)
plt.legend(fontsize=12)
plt.grid(True, which='both', linestyle=':', alpha=0.5)
plt.xlim(2, 2500)

# 残差（ズレ）を計算して表示するサブプロット（オプション：今回はメインのみ）
plt.savefig("yoshimura_victory.png")
print("\n【完了】 最終比較図 'yoshimura_victory.png' を生成しました！")
