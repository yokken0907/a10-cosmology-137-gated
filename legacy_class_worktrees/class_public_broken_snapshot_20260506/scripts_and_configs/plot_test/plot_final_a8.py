import matplotlib.pyplot as plt
import numpy as np
import os

def load_latest(prefix):
    for i in range(5, -1, -1):
        fname = f"{prefix}_{i:02d}_cl.dat"
        if os.path.exists(fname):
            return np.loadtxt(fname)
    return None

std = load_latest("std")
a7 = load_latest("yoshi_a7")
a8 = load_latest("yoshi_a8")

plt.figure(figsize=(12, 7))

# 標準モデル（漆黒の点線）
if std is not None:
    plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM ($H_0=67.4$)", alpha=0.7, linewidth=1.5)

# A7モデル（緑：前回の過程）
if a7 is not None:
    plt.plot(a7[:,0], a7[:,1], 'g:', label="A7 (Step: Reduced Amplitude)", alpha=0.4)

# A8モデル（鮮やかなオレンジの実線：最終解答）
if a8 is not None:
    plt.plot(a8[:,0], a8[:,1], color='orange', label="Yoshimura A8 ($H_0=73.0$ Final)", linewidth=2.5)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura Model A8: The Convergence to Reality")
plt.legend()
plt.grid(True, which='both', linestyle=':', alpha=0.4)
plt.xlim(2, 2500)

plt.savefig("yoshimura_a8_final.png")
print("\n【完了】 最終比較図 'yoshimura_a8_final.png' を生成しました！")
