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
a8  = load_data("yoshi_a8_00_cl.dat") # 前回の現象論モデル
a9  = load_data("yoshi_a9_00_cl.dat") # 今回の正統物理モデル

plt.figure(figsize=(12, 7))

# 標準モデル（黒の点線）
if std is not None:
    plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM ($H_0=67.4$)", alpha=0.6)

# A8（オレンジの薄い線：目標とした現象論的ベストフィット）
if a8 is not None:
    plt.plot(a8[:,0], a8[:,1], color='orange', linestyle=':', label="A8 (Phenomenological Target)", alpha=0.8, linewidth=2)

# A9（赤の太線：今回の二流体・物理モデル）
if a9 is not None:
    plt.plot(a9[:,0], a9[:,1], color='red', label="Yoshimura A9 (Two-Fluid Physical Model, $H_0=73$)", linewidth=2.5)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura A9: From Hack to Physical Theory")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(2, 2500)

plt.savefig("yoshimura_a9_physics.png")
print("\n【完了】 比較グラフ 'yoshimura_a9_physics.png' を生成しました！")
