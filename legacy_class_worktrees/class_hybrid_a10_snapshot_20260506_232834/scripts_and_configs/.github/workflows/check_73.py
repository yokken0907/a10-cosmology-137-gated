from classy import Class
import numpy as np

# 1. 宇宙モデルの設定
cosmo = Class()
params = {
    # --- 基本パラメータ (Planck2018ベース) ---
    #'h': 0.674, 
    'h': 0.731,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'A_s': 2.1e-9,
    'n_s': 0.965,
    'tau_reio': 0.054,

    # --- A10 (初期宇宙の土台) ---
    # ここは前回のMCMCの暫定ベスト付近を設定
    'has_unified_a10': 'yes',
    'ua10_f_ax': 0.22, # 2%の注入
    'ua10_phi_trigger': 0.5,
    
    # --- Factor X (今回実装した最新パーツ) ---
    'has_ua10_tx': 'yes',
    'ua10_tx_omega0': 0.042,  # 現代の寄与 4.5%
    'ua10_tx_zt': 0.035,      # 11億年前の遷移
    'ua10_tx_sigma': 0.04,    # 遷移の鋭さ
    'ua10_tx_dw': -0.60,      # wを一時的に-1.42へ落とす
    
    'output': 'tCl,pCl,lCl,mPk',
    'P_k_max_1/Mpc': 1.0,
}

# 2. 計算実行
print("\n--- 宇宙論エンジンの始動 ---")
cosmo.set(params)
cosmo.compute()

# 3. 結果の抽出
h_derived = cosmo.h()
H0_derived = h_derived * 100
rs_d = cosmo.rs_drag()

print(f"目的地のハッブル定数 H0: 73.0 付近")
print(f"現在の計算結果     H0: {H0_derived:.4f} km/s/Mpc")
print(f"音の地平線尺度     rs: {rs_d:.4f} Mpc")

# 4. BAOの壁チェック (z=0.5付近の距離指標)
# LCDM(H0=67)でのDA/rdは約9.30程度です
z_test = 0.5
da_rd = cosmo.angular_distance(z_test) / rs_d
print(f"z={z_test} での BAO指標: {da_rd:.4f} (ここがLCDMから1%以内なら勝利)")

cosmo.struct_cleanup()
cosmo.empty()