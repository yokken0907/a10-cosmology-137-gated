import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# ファイルパス（A10と標準モデル）
A10_FILE = 'output/project137_16_cl.dat'
STD_FILE = 'output/std_base_00_cl.dat' 

# フォルダの中から「_cl.dat」で終わるファイルを自動で探し出す関数
def find_cl_file(folder_path):
    folder = Path(folder_path)
    cl_files = list(folder.glob('*cl.dat'))
    if not cl_files:
        raise FileNotFoundError(f"😭 {folder_path} の中に cl.dat が見つかりません！")
    return cl_files[0]

def load_cls(path):
    data = np.loadtxt(path)
    ell = data[:, 0]
    tt = data[:, 1]
    return ell, tt

def main():
    # dNeffモデルのファイルを自動検索
    try:
        DNEFF_FILE = find_cl_file('outputs/dneff_grid/Neff3.20_h0.700/')
        print(f"📁 見つけました: {DNEFF_FILE}")
    except Exception as e:
        print(e)
        return

    ell_a10, tt_a10 = load_cls(A10_FILE)
    ell_dn, tt_dn = load_cls(DNEFF_FILE)
    
    # 標準モデルがあれば読み込む
    has_std = False
    if Path(STD_FILE).exists():
        ell_std, tt_std = load_cls(STD_FILE)
        has_std = True

    fig, ax = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    # --- 上段：TTスペクトルの重ね描き ---
    if has_std:
        ax[0].plot(ell_std, tt_std, 'k-', label=r'Standard $\Lambda$CDM ($h=0.67$)', lw=1.5, alpha=0.5)
    
    ax[0].plot(ell_dn, tt_dn, 'r--', label=r'Simple $\Delta N_{eff}$ ($N_{eff}=3.2, H_0=70$)', lw=2)
    ax[0].plot(ell_a10, tt_a10, 'cyan', label=r'A10 Model ($H_0=72$, Triggered)', lw=2)
    
    ax[0].set_ylabel(r'$D_\ell^{TT}$', fontsize=14)
    ax[0].set_yscale('log')
    ax[0].set_xlim(2, 2500)
    ax[0].legend(fontsize=12)
    ax[0].set_title('Acoustic Peak Shift: A10 vs Simple Dark Radiation', fontsize=15)

    # --- 下段：A10を基準とした相対差分 ---
    residual = (tt_dn - tt_a10) / tt_a10
    ax[1].plot(ell_a10, residual, color='magenta', lw=1.5)
    ax[1].axhline(0, color='k', linestyle='--', alpha=0.5)
    ax[1].set_ylabel(r'Rel. Diff $(D_\ell^{\Delta Neff} - D_\ell^{A10}) / D_\ell^{A10}$', fontsize=12)
    ax[1].set_xlabel(r'Multipole $\ell$', fontsize=14)
    ax[1].set_ylim(-0.2, 0.2)
    ax[1].grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('Checkmate_A10_vs_dNeff.png', dpi=300)
    print("✅ 比較グラフ『Checkmate_A10_vs_dNeff.png』を作成しました！")

if __name__ == "__main__":
    main()