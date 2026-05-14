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
a5 = load_latest("yoshi_a5")
a6 = load_latest("yoshi_a6")

plt.figure(figsize=(12, 7))
if std is not None:
    plt.plot(std[:,0], std[:,1], 'k--', label="Standard ($H_0=67.4, age=13.8Gyr$)", alpha=0.5)
if a5 is not None:
    plt.plot(a5[:,0], a5[:,1], 'r:', label="A5 (Old Tilt)", alpha=0.4)
if a6 is not None:
    plt.plot(a6[:,0], a6[:,1], 'b-', label="A6 (New Tilt $n_s=0.945, age=13.0Gyr$)", linewidth=2.5)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura A6: The Rejuvenated Universe")
plt.legend()
plt.grid(True, alpha=0.2)
plt.xlim(2, 2500)
plt.savefig("yoshimura_a6_victory.png")
print("\n【完了】 比較図 'yoshimura_a6_victory.png' を生成しました！")
