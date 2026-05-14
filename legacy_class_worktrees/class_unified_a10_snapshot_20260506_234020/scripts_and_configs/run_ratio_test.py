import matplotlib.pyplot as plt
import numpy as np
from classy import Class

def get_cl_tt(params, label):
    print(f"⌛ {label} を計算中...")
    cosmo = Class()
    cosmo.set(params)
    try:
        cosmo.compute()
        cl = cosmo.raw_cl(2500)
        ell = cl['ell'][2:] 
        cl_tt = cl['tt'][2:]
        print(f"   Done.")
        return ell, cl_tt
    finally:
        cosmo.struct_cleanup()
        cosmo.empty()

# --- 1. 標準モデル (mPkを削除し軽量化) ---
params_lcdm = {
    'H0': 67.4, 'omega_b': 0.0224, 'omega_cdm': 0.120,
    'tau_reio': 0.054, 'A_s': 2.1e-9, 'n_s': 0.965,
    'output': 'tCl', 'l_max_scalars': 2500 # mPkを消しました
}

# --- 2. 究極の Unified A10 (mPkを削除し軽量化) ---
params_a10 = {
    '100*theta_s': 1.0415, 'omega_b': 0.0224, 'omega_cdm': 0.120,
    'tau_reio': 0.054, 'A_s': 2.1e-9, 'n_s': 0.965,
    'has_unified_a10': 'yes', 'ua10_n_ax': 2.5, 'ua10_f_ax': 0.25,
    'ua10_V0': 1.9e-4, 'ua10_Gamma0': 0.55,
    'ua10_phi_trigger': 1e-6, 'ua10_Delta_phi': 0.60,
    'output': 'tCl', 'l_max_scalars': 2500 # mPkを消しました
}

# 計算実行
ell, cl_lcdm = get_cl_tt(params_lcdm, "Standard LCDM")
_, cl_a10 = get_cl_tt(params_a10, "Unified A10")

# --- Ratio プロット ---
ratio = cl_a10 / cl_lcdm
plt.figure(figsize=(10, 6))
plt.plot(ell, ratio, 'm-', lw=2, label=r'$R_\ell \equiv C_\ell^{\rm A10} / C_\ell^{\rm \Lambda CDM}$')
plt.axhline(1.0, color='k', linestyle='-')
plt.axhline(1.02, color='r', linestyle='--', alpha=0.3)
plt.axhline(0.98, color='r', linestyle='--', alpha=0.3)
plt.fill_between(ell, 0.98, 1.02, color='gray', alpha=0.1, label='Planck Safe Zone (2%)')
plt.ylim(0.95, 1.05)
plt.title("The Ultimate Test: CMB Ratio Plot")
plt.legend()
plt.grid(alpha=0.2)
plt.savefig("the_ratio_test.png", dpi=300)
print("\n✅ 'the_ratio_test.png' を生成しました。今度こそ通ったはずです！")