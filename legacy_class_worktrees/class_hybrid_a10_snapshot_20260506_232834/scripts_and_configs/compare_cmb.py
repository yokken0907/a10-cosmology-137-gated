import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# --- 最新の2つのデータファイルを自動で探す ---
files = glob.glob('output/a10_test_*_cl.dat')
files.sort(key=os.path.getmtime) # 更新日時でソート

if len(files) < 2:
    print("比較には少なくとも2つのデータファイルが必要です。")
    exit()

# 最新（今実行したドラッグなし）と、その前（ドラッグあり）を取得
standard_file = files[-1]
a10_file = files[-2]

print(f"📡 比較中:")
print(f"  [A] A10 Model: {a10_file}")
print(f"  [B] Standard (no drag): {standard_file}")

# データの読み込み
data_a10 = np.genfromtxt(a10_file, comments='#')
data_std = np.genfromtxt(standard_file, comments='#')

l_a10, tt_a10 = data_a10[:, 0], data_a10[:, 1]
l_std, tt_std = data_std[:, 0], data_std[:, 1]

# --- グラフ描画 ---
plt.figure(figsize=(12, 7))

# メインの比較
plt.plot(l_std, tt_std, 'k--', label='Standard LCDM (Gamma=0)', alpha=0.8)
plt.plot(l_a10, tt_a10, 'r-', label='Unified A10 Model (137 Gate)', linewidth=2)

plt.xscale('log')
plt.xlabel('Multipole Moment (l)')
plt.ylabel(r'$l(l+1)C_l^{TT} / 2\pi$ [$\mu K^2$]')
plt.title('CMB Power Spectrum Comparison')
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.legend()

# ズレを強調するための残差プロットを右上に挿入するなどの工夫も可能ですが、
# まずは単純に重ねてみましょう。

plt.savefig('cmb_comparison.png', dpi=300)
print("🌠 比較グラフを 'cmb_comparison.png' に保存しました！")