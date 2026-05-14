import numpy as np
import matplotlib.pyplot as plt
import os

# 視覚的疲労軽減のための設定
plt.style.use('dark_background')

# ファイルパスの指定
data_file = 'output/a10_test_background.dat'

if not os.path.exists(data_file):
    print(f"エラー: {data_file} が見つかりません。計算が失敗している可能性があります。")
else:
    # データの読み込み (CLASSの出力は通常、先頭数行がコメント)
    # 1列目: z (赤方偏移), 3列目: H [1/Mpc]
    data = np.loadtxt(data_file)
    z = data[:, 0]
    H = data[:, 2]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # ハッブルパラメータ H(z) のプロット
    ax.plot(z, H, color='cyan', label='A10 Model (RBH Coupling)', linewidth=2)
    
    ax.set_xlabel('Redshift $z$')
    ax.set_ylabel('Hubble Parameter $H(z)$ [1/Mpc]')
    ax.set_title('Cosmological Expansion with RBH Coupling')
    ax.set_xlim(0, 2)  # 近傍宇宙にフォーカス
    ax.grid(True, alpha=0.3)
    ax.legend()

    output_plot = 'a10_expansion_result.png'
    plt.savefig(output_plot)
    print(f"プロットを保存しました: {output_plot}")
    plt.show()