import matplotlib.pyplot as plt
import numpy as np
import os

# 確実に存在する「00」番のファイルを指定
std_file = "std_00_cl.dat"
yoshi_file = "yoshi_00_cl.dat"

print(f"Reading {std_file} and {yoshi_file}...")

# データの読み込み
try:
    std = np.loadtxt(std_file)
    yoshi = np.loadtxt(yoshi_file)

    plt.figure(figsize=(10, 6))
    
    # 標準モデル (黒の点線)
    plt.plot(std[:,0], std[:,1], 'k--', label="Standard LCDM ($H_0=67.4$)", alpha=0.7)
    
    # 吉村モデル (赤の実線)
    plt.plot(yoshi[:,0], yoshi[:,1], 'r-', label="Yoshimura A1 Model ($H_0=72.6$)", linewidth=2)

    plt.xlabel(r"Multipole $\ell$")
    plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
    plt.title("Final Comparison: CMB Power Spectrum")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.xlim(2, 2500)

    output_img = "comparison_result.png"
    plt.savefig(output_img)
    print(f"\n【祝】 グラフ '{output_img}' を生成しました！")

except Exception as e:
    print(f"\n【エラー】読み込みに失敗しました: {e}")
    print("ファイルが壊れているか、中身が空かもしれません。")
