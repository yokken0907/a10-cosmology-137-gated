import numpy as np
import matplotlib.pyplot as plt
import glob
import os

plt.style.use('dark_background')

# 最新のファイルを探す
list_of_files = glob.glob('output/*_background.dat')
if not list_of_files:
    print("データが見つかりません。")
else:
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"最新のデータを解析中: {latest_file}")

    data = np.loadtxt(latest_file)
    z = data[:, 0]
    H = data[:, 3] # 4列目: H [1/Mpc]

    # 【重要】赤方偏移 z が 0 から 2 の範囲だけを抜き出す
    mask = (z >= 0) & (z <= 2)
    z_zoom = z[mask]
    H_zoom = H[mask]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # プロット (単位を分かりやすくするため、H0 で規格化するかそのまま出すか)
    ax.plot(z_zoom, H_zoom, color='springgreen', label='A10 Model (k=1.1)', linewidth=2.5)
    
    ax.set_xlabel('Redshift $z$', fontsize=12)
    ax.set_ylabel('$H(z)$ [1/Mpc]', fontsize=12)
    ax.set_title('Hubble Expansion in Late Universe (z < 2)', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend()

    plt.savefig('a10_zoomed_H_plot.png')
    print("拡大プロットを保存しました: a10_zoomed_H_plot.png")