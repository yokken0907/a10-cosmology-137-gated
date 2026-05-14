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
a6 = load_latest("yoshi_a6")
a7 = load_latest("yoshi_a7")

plt.figure(figsize=(12, 7))

# 標準モデル（グレー点線）
if std is not None:
    plt.plot(std[:,0], std[:,1], 'k--', label="Standard ($H_0=67.4$)", alpha=0.6)

# A6モデル（青：前回の失敗作）
if a6 is not None:
    plt.plot(a6[:,0], a6[:,1], 'b:', label="A6 (Too energetic)", alpha=0.4)

# A7モデル（緑：今回の本命）
if a7 is not None:
    plt.plot(a7[:,0], a7[:,1], 'g-', label="Yoshimura A7 ($H_0=73.0, A_s$ reduced)", linewidth=2.5)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura A7: Balancing Amplitude with Energy Injection")
plt.legend()
plt.grid(True, alpha=0.2)
plt.xlim(2, 2500)

plt.savefig("yoshimura_a7_comparison.png")
print("\n【完了】 比較図 'yoshimura_a7_comparison.png' を生成しました！")
