import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# 最新の _cl.dat ファイルを探す
files = glob.glob('output/a10_test_*_cl.dat')
if not files:
    print("CMBデータファイルが見つかりません。")
    exit()
latest_cl = max(files, key=os.path.getctime)
print(f"📡 観測対象: {latest_cl}")

# データの読み込み
# 1列目: l, 2列目: TTスペクトル
data = np.genfromtxt(latest_cl, comments='#')
l = data[:, 0]
tt = data[:, 1]

plt.figure(figsize=(10, 6))
plt.plot(l, tt, label='Unified A10 Model', color='blue', linewidth=2)

plt.xscale('log')
plt.xlabel('Multipole Moment (l)')
plt.ylabel(r'$l(l+1)C_l^{TT} / 2\pi$ [$\mu K^2$]')
plt.title('CMB Temperature Power Spectrum with 137 Gate')
plt.grid(True, which="both", ls="-", alpha=0.3)
plt.legend()

plt.savefig('cmb_spectrum_a10.png', dpi=300)
print("🌠 グラフを 'cmb_spectrum_a10.png' に保存しました！")