import matplotlib.pyplot as plt
import numpy as np

# 存在するファイルを読み込むだけ！
d_std = np.loadtxt("std_cl.dat")
d_yoshi = np.loadtxt("yoshi_cl.dat")

plt.figure(figsize=(10, 6))
plt.plot(d_std[:,0], d_std[:,1], 'k--', label="Standard ($H_0=67$)")
plt.plot(d_yoshi[:,0], d_yoshi[:,1], 'r-', label="Yoshimura ($H_0=73$)", linewidth=2)

plt.xlabel("Multipole l")
plt.ylabel("l(l+1)Cl/2pi")
plt.legend()
plt.savefig("yoshimura_final.png")
print("できました！ yoshimura_final.png を確認してください。")
