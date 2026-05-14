import matplotlib.pyplot as plt
import numpy as np
from classy import Class

def run_ultimate_check():
    # --- 1. 黄金モデル (Unified A10) の計算 ---
    print("🚀 究極の Unified A10 モデルを計算中...")
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
        'ua10_V0': 1.9e-4,
        'ua10_Gamma0': 0.62,
        'ua10_phi_trigger': 1e-6,
        'ua10_Delta_phi': 0.60,
        'output': 'tCl, mPk',
        'l_max_scalars': 2500
    })
    
    try:
        a10.compute()
        h0 = a10.h() * 100
        sigma8 = a10.sigma8()
        omega_m = a10.Omega_m()
        s8 = sigma8 * (omega_m / 0.3)**0.5
        
        print(f"\n--- 🏆 究極診断結果 ---")
        print(f"H0: {h0:.4f}")
        print(f"S8: {s8:.4f}")
        print(f"rs_d: {a10.rs_drag():.2f} Mpc")
        
        # 波形データの保存
        cl_a10 = a10.raw_cl(2500)
        ll = cl_a10['ell']
        factor = ll*(ll+1)/(2*np.pi) * 1e12 * (2.7255)**2
        tt_a10 = factor * cl_a10['tt']
        
        # 計算が終わったら即座にメモリ解放（Segfault防止）
        a10.struct_cleanup(); a10.empty()
        
        return ll, tt_a10, h0, s8

    except Exception as e:
        print(f"❌ 計算失敗: {e}")
        return None

# 実行
result = run_ultimate_check()

if result:
    ll, tt_a10, h0, s8 = result
    plt.figure(figsize=(10, 6))
    plt.plot(ll, tt_a10, 'r-', label=f'Unified A10 (H0={h0:.2f}, S8={s8:.3f})')
    plt.title("Ultimate Solution of Cosmological Tensions")
    plt.xlabel(r"Multipole $\ell$")
    plt.ylabel(r"$D_\ell^{TT} \quad [\mu K^2]$")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.savefig("The_Final_Universe.png", dpi=300)
    print("\n✅ 全工程完了。'The_Final_Universe.png' を確認してください。")