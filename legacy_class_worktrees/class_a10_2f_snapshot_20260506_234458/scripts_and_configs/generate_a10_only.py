import matplotlib.pyplot as plt
import numpy as np
from classy import Class

print("🚀 黄金モデル (Unified A10) 単独突破作戦を開始...")

a10 = Class()
a10.set({
    '100*theta_s': 1.0411,
    'omega_b': 0.0224,
    'omega_cdm': 0.120,
    'tau_reio': 0.054,
    'A_s': 2.1e-9,
    'n_s': 0.965,
    'has_unified_a10': 'yes',
    'ua10_n_ax': 2.5,
    'ua10_f_ax': 0.25,
    'ua10_V0': 2.0e-4,
    'ua10_Gamma0': 0.65,
    'ua10_phi_trigger': 1e-6,
    'ua10_Delta_phi': 0.60,
    'output': 'tCl',
    'l_max_scalars': 2500
})

try:
    # メモリが綺麗な状態で、真っ先に A10 を計算
    a10.compute()
    print("✅ 計算成功！ H0 =", a10.h()*100)
    
    cl_a10 = a10.raw_cl(2500)
    ll = cl_a10['ell']
    factor = ll*(ll+1)/(2*np.pi) * 1e12 * (2.7255)**2 

    plt.figure(figsize=(10, 6))
    plt.plot(ll, factor*cl_a10['tt'], 'r-', label='Unified A10 (H0=73.14)')
    plt.xlabel(r'Multipole $\ell$')
    plt.ylabel(r'$D_\ell^{TT} \quad [\mu K^2]$')
    plt.title("The Golden Universe: Unified A10 Spectrum")
    plt.legend()
    plt.grid(alpha=0.3)
    
    plt.savefig("a10_single_victory.png", dpi=300)
    print("✅ グラフ保存完了: a10_single_victory.png")

except Exception as e:
    print(f"❌ 単独計算でも失敗:\n{e}")

a10.struct_cleanup(); a10.empty()