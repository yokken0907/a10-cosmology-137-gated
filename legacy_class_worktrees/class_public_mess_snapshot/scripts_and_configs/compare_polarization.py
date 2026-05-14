import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# ファイルパス（TTの時と同じです）
A10_FILE = 'output/project137_16_cl.dat'
STD_FILE = 'output/std_base_00_cl.dat' 

def find_cl_file(folder_path):
    folder = Path(folder_path)
    cl_files = list(folder.glob('*cl.dat'))
    if not cl_files:
        raise FileNotFoundError(f"😭 {folder_path} の中に cl.dat が見つかりません！")
    return cl_files[0]

def load_cls(path):
    data = np.loadtxt(path)
    ell = data[:, 0]
    # 偏光データは 2列目(EE) と 3列目(TE) にあります
    ee = data[:, 2]
    te = data[:, 3]
    return ell, ee, te

def plot_ee(ell_std, ee_std, ell_a10, ee_a10, ell_dn, ee_dn):
    fig, ax = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    ax[0].plot(ell_std, ee_std, 'k-', label=r'Standard $\Lambda$CDM ($h=0.67$)', lw=1.5, alpha=0.5)
    ax[0].plot(ell_dn, ee_dn, 'r--', label=r'Simple $\Delta N_{eff}$ ($N_{eff}=3.2, H_0=70$)', lw=2)
    ax[0].plot(ell_a10, ee_a10, 'cyan', label=r'A10 Model ($H_0=72$, Triggered)', lw=2)
    
    ax[0].set_ylabel(r'$D_\ell^{EE}$', fontsize=14)
    ax[0].set_yscale('log')
    ax[0].set_xlim(2, 2500)
    ax[0].legend(fontsize=12)
    ax[0].set_title('Polarization EE Spectrum: A10 vs Simple Dark Radiation', fontsize=15)

    # EEの相対差分
    residual = (ee_dn - ee_a10) / ee_a10
    ax[1].plot(ell_a10, residual, color='magenta', lw=1.5)
    ax[1].axhline(0, color='k', linestyle='--', alpha=0.5)
    ax[1].set_ylabel(r'Rel. Diff $(EE^{\Delta Neff} - EE^{A10}) / EE^{A10}$', fontsize=10)
    ax[1].set_xlabel(r'Multipole $\ell$', fontsize=14)
    ax[1].set_ylim(-0.2, 0.2)
    ax[1].grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('Checkmate_EE.png', dpi=300)
    plt.close()

def plot_te(ell_std, te_std, ell_a10, te_a10, ell_dn, te_dn):
    fig, ax = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    ax[0].plot(ell_std, te_std, 'k-', label=r'Standard $\Lambda$CDM ($h=0.67$)', lw=1.5, alpha=0.5)
    ax[0].plot(ell_dn, te_dn, 'r--', label=r'Simple $\Delta N_{eff}$ ($N_{eff}=3.2, H_0=70$)', lw=2)
    ax[0].plot(ell_a10, te_a10, 'cyan', label=r'A10 Model ($H_0=72$, Triggered)', lw=2)
    
    ax[0].set_ylabel(r'$D_\ell^{TE}$', fontsize=14)
    ax[0].set_xlim(2, 2500)
    # TEはマイナスになるので log スケールは使いません
    ax[0].legend(fontsize=12)
    ax[0].set_title('Polarization TE Spectrum: A10 vs Simple Dark Radiation', fontsize=15)

    # TEの絶対差分（ゼロクロスがあるため）
    abs_diff = te_dn - te_a10
    ax[1].plot(ell_a10, abs_diff, color='magenta', lw=1.5)
    ax[1].axhline(0, color='k', linestyle='--', alpha=0.5)
    ax[1].set_ylabel(r'Abs. Diff $TE^{\Delta Neff} - TE^{A10}$', fontsize=10)
    ax[1].set_xlabel(r'Multipole $\ell$', fontsize=14)
    ax[1].grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('Checkmate_TE.png', dpi=300)
    plt.close()

def main():
    DNEFF_FILE = find_cl_file('outputs/dneff_grid/Neff3.20_h0.700/')
    ell_a10, ee_a10, te_a10 = load_cls(A10_FILE)
    ell_dn, ee_dn, te_dn = load_cls(DNEFF_FILE)
    
    if Path(STD_FILE).exists():
        ell_std, ee_std, te_std = load_cls(STD_FILE)
    else:
        print("標準モデルが見つからないため、黒線なしでプロットします。")
        ell_std, ee_std, te_std = ell_a10, np.zeros_like(ee_a10), np.zeros_like(te_a10)
    
    plot_ee(ell_std, ee_std, ell_a10, ee_a10, ell_dn, ee_dn)
    plot_te(ell_std, te_std, ell_a10, te_a10, ell_dn, te_dn)
    print("✅ 偏光グラフ『Checkmate_EE.png』と『Checkmate_TE.png』を2枚作成しました！")

if __name__ == "__main__":
    main()