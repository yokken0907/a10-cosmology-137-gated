import matplotlib.pyplot as plt
import numpy as np

# 存在するファイルを正確に指定
std_file = "std_00_cl.dat"
yoshi_a1_file = "yoshi_00_cl.dat"
yoshi_a2_file = "yoshi_a2_01_cl.dat" # 最新の01番を使用

print(f"Loading files: {std_file}, {yoshi_a1_file}, {yoshi_a2_file}")

# データの読み込み
std = np.loadtxt(std_file)
yoshi_a1 = np.loadtxt(yoshi_a1_file)
yoshi_a2 = np.loadtxt(yoshi_a2_file)

plt.figure(figsize=(10, 6))

# 標準モデル (グレーの点線)
plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM", alpha=0.5)

# A1モデル (赤の点線)
plt.plot(yoshi_a1[:,0], yoshi_a1[:,1], 'r:', label="Yoshimura A1 (H0=72.6)")

# A2モデル (青の実線) - 今回の修正版
plt.plot(yoshi_a2[:,0], yoshi_a2[:,1], 'b-', label="Yoshimura A2 (H0=71.5)", linewidth=2)

plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
plt.title("Cosmological Model Evolution: Toward the Perfect Fit")
plt.legend()
plt.grid(True, alpha=0.2)
plt.xlim(2, 2500)

plt.savefig("evolution_result.png")
print("\n【大成功】 比較図 'evolution_result.png' を生成しました！")
