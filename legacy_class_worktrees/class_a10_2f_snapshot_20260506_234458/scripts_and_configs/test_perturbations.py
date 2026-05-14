from classy import Class

cosmo = Class()
params = {
    # --- 基本パラメータ ---
    'h': 0.724, 
    'omega_b': 0.02237, 
    'omega_cdm': 0.1400, # ChatGPT指摘の高cdm
    'A_s': 2.1e-9, 
    'n_s': 0.965, 
    'tau_reio': 0.054,
    
    # --- A10 初期ブースト ---
    'has_unified_a10': 'yes',
    'ua10_f_ax': 0.12, 
    'ua10_phi_trigger': 0.5,

    # --- 乗っ取った公式 fld (Factor X) ---
    'Omega_fld': 0.042,                 # これが昔の ua10_tx_omega0
    'fluid_equation_of_state': 'ua10tx',# 新たに定義したUA10TXモード
    'ua10_tx_zt': 0.10,
    'ua10_tx_sigma': 0.04,
    'ua10_tx_dw': -0.40,
    
    # --- 摂動(揺らぎ)を安全に計算するための魔法のお守り ---
    'use_ppf': 'no',                    # 爆弾（不良品）なので OFF！
    'cs2_fld': 1.0,                     # 音速を光速（1.0）にして揺らぎの発散を防ぐ！
    'recombination': 'recfast',
    
    # 出力設定
    'output': 'tCl,pCl,lCl,mPk',
    'l_max_scalars': 2500,
    'P_k_max_1/Mpc': 1.0,
}

print("--- A10 ハイブリッド：摂動(Perturbations) 突破テスト ---")
try:
    cosmo.set(params)
    cosmo.compute()
    print("✅ 大成功！摂動(CMB・物質パワースペクトル)の計算をエラーなしで突破しました！")
    print(f"H0: {cosmo.h()*100:.2f}")
    print(f"rs: {cosmo.rs_drag():.2f}")
except Exception as e:
    print("❌ エラー発生:")
    print(e)

cosmo.struct_cleanup()
cosmo.empty()