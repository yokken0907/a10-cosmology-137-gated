import matplotlib.pyplot as plt
import numpy as np
import os

files = {
    "Standard": "std_00_cl.dat",
    "A1 (Initial)": "yoshi_00_cl.dat",
    "A3 (Mass Adj)": "yoshi_a3_00_cl.dat",
    "A4 (Time Shift)": "yoshi_a4_00_cl.dat"
}

plt.figure(figsize=(12, 7))
colors = ["gray", "red", "green", "blue"]
styles = ["--", ":", "-.", "-"]

for (label, f), color, ls in zip(files.items(), colors, styles):
    if os.path.exists(f):
        data = np.loadtxt(f)
        lw = 3 if "A4" in label else 1.5
        plt.plot(data[:,0], data[:,1], label=label, color=color, linestyle=ls, linewidth=lw)
    else:
        print(f"Warning: {f} not found.")

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Yoshimura Model Evolution: Shifting the Injection Time")
plt.legend()
plt.grid(True, alpha=0.2)
plt.xlim(2, 2500)
plt.savefig("a4_comparison.png")
print("\n【完了】 A4比較グラフ 'a4_comparison.png' を生成しました！")
