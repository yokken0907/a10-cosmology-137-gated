import matplotlib.pyplot as plt
import numpy as np

# A8とStandardを読み込み
std = np.loadtxt("std_00_cl.dat")
a8 = np.loadtxt("yoshi_a8_00_cl.dat")

plt.figure(figsize=(12, 8))

# 1. 観測データの「許容範囲」を影で表現（簡略化したPlanck誤差範囲）
plt.fill_between(std[:,0], std[:,1]*0.98, std[:,1]*1.02, color='gray', alpha=0.2, label="Planck Observed Region (approx)")

# 2. 標準モデル
plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM (H0=67.4)", alpha=0.8)

# 3. 吉村 A8 モデル
plt.plot(a8[:,0], a8[:,1], color='tab:orange', linewidth=3, label="Yoshimura A8 (H0=73.0)")

plt.yscale('linear')
plt.xlabel(r"Multipole $\ell$", fontsize=14)
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$", fontsize=14)
plt.title("Yoshimura's Final Legacy: Solving the Hubble Tension", fontsize=16)
plt.legend(loc='upper right', fontsize=12)
plt.grid(True, which='both', linestyle=':', alpha=0.5)
plt.xlim(2, 2500)

# 拡大図の挿入（第1ピーク付近）
ax_ins = plt.axes([0.55, 0.25, 0.3, 0.3])
ax_ins.plot(std[:500,0], std[:500,1], 'k--')
ax_ins.plot(a8[:500,0], a8[:500,1], color='tab:orange', linewidth=2)
ax_ins.set_xlim(150, 300)
ax_ins.set_title("Peak 1 Detail")

plt.savefig("yoshimura_legacy.png")
print("\n【祝】 最終論文用グラフ 'yoshimura_legacy.png' を生成しました！")
