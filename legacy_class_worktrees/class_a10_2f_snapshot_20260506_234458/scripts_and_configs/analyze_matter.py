# analyze_matter.py として実行
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# 最新の _pk.dat を取得
files = glob.glob('output/a10_test_*_pk.dat')
files.sort(key=os.path.getmtime)
pk_std, pk_a10 = files[-1], files[-2]

data_std = np.genfromtxt(pk_std)
data_a10 = np.genfromtxt(pk_a10)

k = data_std[:, 0]
ps_std = data_std[:, 1]
ps_a10 = data_a10[:, 1]

plt.figure(figsize=(10, 6))
# ズレの比率を表示
plt.plot(k, (ps_a10 - ps_std) / ps_std * 100, color='green')
plt.xscale('log')
plt.ylabel('Matter Power Difference [%]')
plt.xlabel('Wavenumber k [1/Mpc]')
plt.title('Impact on Galaxy Distribution (137 Gate)')
plt.grid(True, alpha=0.3)
plt.savefig('matter_analysis.png')
print("🌌 物質分布への影響を 'matter_analysis.png' に保存しました。")