import matplotlib.pyplot as plt
import numpy as np
import os

def load_data(filename):
    if os.path.exists(filename):
        return np.loadtxt(filename)
    else:
        print(f"Warning: {filename} not found!")
        return None

# データの読み込み
std = load_data("std_00_cl.dat")
a9  = load_data("yoshi_a9_00_cl.dat")  # 前回の背景のみモデル
a10 = load_data("yoshi_a10_00_cl.dat") # 今回の完全物理モデル

plt.figure(figsize=(12, 7))

# 標準モデル（黒の点線）
if std is not None:
    plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM ($H_0=67.4$)", alpha=0.6)

# A9（赤の点線：摂動なしのベースライン）
if a9 is not None:
    plt.plot(a9[:,0], a9[:,1], color='red', linestyle=':', label="A9 (Background Only, $H_0=73$)", alpha=0.7, linewidth=2)

# A10（青の太線：真の物理モデル）
if a10 is not None:
    plt.plot(a10[:,0], a10[:,1], color='blue', label="Yoshimura A10 (Full Physics, $H_0=73$)", linewidth=2.5)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura A10: The Ultimate Physical Model")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(2, 2500)

plt.savefig("yoshimura_a10_full_physics.png")
print("\n【完了】 比較グラフ 'yoshimura_a10_full_physics.png' を生成しました！")
