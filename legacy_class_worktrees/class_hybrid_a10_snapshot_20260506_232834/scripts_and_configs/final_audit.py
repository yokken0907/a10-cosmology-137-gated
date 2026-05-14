import numpy as np
from classy import Class

# ==========================================
# 1. 標準パラメータ (Standard LCDM)
# ==========================================
params_std = {
    'output': 'tCl, mPk',
    'l_max_scalars': 2500,
    'P_k_max_h/Mpc': 1.0,
    'gauge': 'newtonian',
    'YHe': 0.2454,
    'recombination': 'RECFAST',  # 外部モジュールのバグ回避用
    
    # H0を計算結果として変動させるため、hではなくプランクの角度スケールを固定
    #'100*theta_s': 1.04119, 
    'h': 0.72,

    'omega_b': 0.02237,
    'omega_cdm': 0.12,
    
    # 微分方程式ソルバーを安定させるための安全装置
    'tol_background_integration': 1e-6,
}

# ==========================================
# 2. 改造モデルパラメータ (Unified A10)
# ==========================================
params_a10 = {
    **params_std,               # 標準パラメータをすべて引き継ぐ
    'has_unified_a10': 'yes',   # A10ロジックをオンにするスイッチ

    'ua10_V0': 1.5e-4,
    'ua10_Delta_phi': 0.60,
    'ua10_phi_trigger': 1e-6,    
    'ua10_Gamma0': 0.005,

    'ua10_n_ax': 2.5,
    'ua10_f_ax': 0.25,
}

# ==========================================
# 3. 診断関数の定義
# ==========================================
def get_diagnostics(p_dict, label):
    print(f"🔭 {label} の計算を開始...")
    cosmo = Class()
    cosmo.set(p_dict)
    cosmo.compute()
    
    h0 = cosmo.h() * 100
    sigma8 = cosmo.sigma8()
    omega_m = cosmo.Omega_m()
    s8 = sigma8 * (omega_m / 0.3)**0.5
    rs = cosmo.rs_drag()
    
    print(f"--- {label} 診断結果 ---")
    print(f"H0:     {h0:.2f}")
    print(f"S8:     {s8:.4f}")
    print(f"sigma8: {sigma8:.4f}")
    print(f"rs_d:   {rs:.2f} Mpc\n")
    
    # メモリの確実な解放
    cosmo.struct_cleanup()
    cosmo.empty()
    
    return h0, s8, rs

# ==========================================
# 4. 実行と判定ブロック
# ==========================================
if __name__ == '__main__':
    try:
        h_std, s_std, r_std = get_diagnostics(params_std, "Standard LCDM")
        h_a10, s_a10, r_a10 = get_diagnostics(params_a10, "Unified A10")

        print("="*40)
        print("📊 FINAL VERDICT: テンション解消の判定")
        print("="*40)
        
        # 判定ロジック
        h_status = "✅ Improved!" if h_a10 > h_std else "❌ Not improved"
        print(f"H0 Tension: {h_status:<15} (Delta H0: {h_a10 - h_std:+.2f})")
        
        s_status = "✅ Improved!" if s_a10 < s_std else "❌ Not improved"
        print(f"S8 Tension: {s_status:<15} (Delta S8: {s_a10 - s_std:+.4f})")
        print("="*40)

    except Exception as e:
        print(f"\n❌ エラーが発生しました:\n{e}")