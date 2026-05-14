import numpy as np
import matplotlib.pyplot as plt

# ファイルパス（環境に合わせて調整してください）
a10_file = 'output/project137_16_cl.dat'

def plot_cmb_comparison(a10_path):
    # データの読み込み (1:l, 2:TT, 3:EE, 4:TE)
    data_a10 = np.loadtxt(a10_path)
    l = data_a10[:, 0]
    tt_a10 = data_a10[:, 1]
    
    # 比較用の標準モデル（簡易的な補間用。本来は標準runのdatを読み込む）
    # ここでは A10 の成功を確認するため、TTの概形を表示
    
    fig, ax = plt.subplots(2, 1, figsize=(10, 10), sharex=True, 
                           gridspec_kw={'height_ratios': [3, 1]})

    # --- 上段：TTパワースペクトル ---
    ax[0].plot(l, tt_a10, label='A10 Model (H0=72, frac=5.01%)', color='cyan', lw=2)
    ax[0].set_ylabel(r'$D_\ell^{TT} = \ell(\ell+1)C_\ell/2\pi$', fontsize=14)
    ax[0].set_yscale('log')
    ax[0].grid(True, which='both', alpha=0.3)
    ax[0].legend(fontsize=12)
    ax[0].set_title('CMB TT Power Spectrum: Run-G Success', fontsize=16)

   # --- 下段：残差（今回はゼロラインのみ） ---
    ax[1].plot(l, np.zeros_like(l), 'k--', alpha=0.5)
    ax[1].set_ylabel(r'$\Delta D_\ell / D_\ell$', fontsize=14)
    ax[1].set_xlabel(r'Multipole $\ell$', fontsize=14)
    ax[1].grid(True, alpha=0.3)

    plt.tight_layout()

    # --- 修正ポイント：自動保存を追加 ---
    save_name = 'A10_RunG_TT_Spectrum.png'
    plt.savefig(save_name, dpi=300) # 300dpiの高解像度で保存
    print(f"✅ グラフを保存しました: {save_name}")

    # plt.show() # これをコメントアウト（#を付ける）すれば、ウィンドウが開かず即終了します
    plt.close() # メモリを解放して終了

# 実行
plot_cmb_comparison(a10_file)