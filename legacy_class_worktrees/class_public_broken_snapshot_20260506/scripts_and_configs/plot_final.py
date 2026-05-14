import matplotlib.pyplot as plt
import numpy as np

# 直接ファイルを指定して読み込む
l_std, tt_std = np.loadtxt("output/std_cl.dat")[:, 0], np.loadtxt("output/std_cl.dat")[:, 1]
l_yoshi, tt_yoshi = np.loadtxt("output/yoshi_cl.dat")[:, 0], np.loadtxt("output/yoshi_cl.dat")[:, 1]

plt.figure(figsize=(10, 6))
plt.plot(l_std, tt_std, label="Standard LCDM ($H_0 \\approx 67$)", color="gray", linestyle="--")
plt.plot(l_yoshi, tt_yoshi, label="Yoshimura A1 Model ($H_0 \\approx 73$)", color="red", linewidth=2)

plt.xlabel("Multipole l")
plt.ylabel("l(l+1)Cl / 2pi")
plt.title("Yoshimura Universe vs Standard Universe")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("yoshimura_final.png")
print("グラフ 'yoshimura_final.png' を生成しました！")
