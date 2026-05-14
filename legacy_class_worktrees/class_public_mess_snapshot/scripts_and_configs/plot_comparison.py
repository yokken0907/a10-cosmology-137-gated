import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # ターミナル占拠防止

# ファイル設定
a10_file = 'output/project137_16_cl.dat'
std_file = 'output/std_base_00_cl.dat'

def analyze_comparison():
    # データ読み込み
    a10 = np.loadtxt(a10_file)
    std = np.loadtxt(std_file)
    
    l = a10[:, 0]
    tt_a10 = a10[:, 1]
    tt_std = std[:, 1] # lの範囲が同じであることを想定

    fig, ax = plt.subplots(2, 1, figsize=(10, 10), sharex=True, 
                           gridspec_kw={'height_ratios': [3, 1]})

    # --- 上段：TTスペクトル 重ね描き ---
    ax[0].plot(l, tt_std, 'k-', label=r'Standard $\Lambda$CDM ($h=0.67$)', lw=1.5, alpha=0.8)
    ax[0].plot(l, tt_a10, 'cyan', label=r'A10 Model ($h=0.72, f=5.01\%$)', lw=2)
    ax[0].set_ylabel(r'$D_\ell^{TT}$', fontsize=14)
    ax[0].set_yscale('log')
    ax[0].legend()
    ax[0].set_title('A10 Model vs Standard LCDM')

    # --- 下段：残差プロット (A10 - Std) / Std ---
    residual = (tt_a10 - tt_std) / tt_std
    ax[1].plot(l, residual, color='magenta', lw=1.5)
    ax[1].axhline(0, color='k', linestyle='--', alpha=0.5)
    ax[1].set_ylabel(r'Relative Diff $\Delta D_\ell / D_\ell$', fontsize=12)
    ax[1].set_xlabel(r'Multipole $\ell$', fontsize=14)
    ax[1].set_ylim(-0.05, 0.05) # ±5%の範囲を表示
    ax[1].grid(True, alpha=0.2)

    plt.tight_layout()
    save_name = 'Comparison_A10_vs_Std.png'
    plt.savefig(save_name, dpi=300)
    print(f"✅ 解析完了。比較図を保存しました: {save_name}")

if __name__ == "__main__":
    analyze_comparison()