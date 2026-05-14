import matplotlib.pyplot as plt
import numpy as np
import os

# ファイル指定（番号は適宜調整してください）
files = {
    "Standard": "std_00_cl.dat",
    "Yoshimura A1": "yoshi_00_cl.dat",
    "Yoshimura A2": "yoshi_a2_01_cl.dat",
    "Yoshimura A3": "yoshi_a3_00_cl.dat" # もしエラーなら01に変更
}

plt.figure(figsize=(12, 7))

# データの読み込みとプロット
colors = ["black", "red", "blue", "green"]
linestyles = ["--", ":", "-.", "-"]

for (label, f), color, ls in zip(files.items(), colors, linestyles):
    if os.path.exists(f):
        data = np.loadtxt(f)
        lw = 2.5 if "A3" in label else 1.5
        alpha = 1.0 if "A3" in label else 0.6
        plt.plot(data[:,0], data[:,1], label=label, color=color, linestyle=ls, linewidth=lw, alpha=alpha)
    else:
        print(f"Warning: {f} not found.")

plt.xlabel(r"Multipole $\ell$", fontsize=12)
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$", fontsize=12)
plt.title("Cosmological Evolution: The Quest for Hubble Tension Solution", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, which='both', linestyle='--', alpha=0.3)
plt.xlim(2, 2500)

plt.savefig("final_showdown.png")
print("\n【完了】 集大成グラフ 'final_showdown.png' を生成しました！")
