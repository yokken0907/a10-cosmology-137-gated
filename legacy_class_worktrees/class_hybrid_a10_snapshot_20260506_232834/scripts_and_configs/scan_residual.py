from classy import Class
import numpy as np

# 共通設定
z_arr = np.linspace(0.01, 2.5, 50) # z=0.01 から 2.5 までを50等分して調べる

# ==========================================
# 1. 基準となる標準理論 (Lambda-CDM) の計算
# ==========================================
cosmo_lcdm = Class()
params_lcdm = {
    'h': 0.674, 'omega_b': 0.02237, 'omega_cdm': 0.1200,
    'A_s': 2.1e-9, 'n_s': 0.965, 'tau_reio': 0.054
}
cosmo_lcdm.set(params_lcdm)
cosmo_lcdm.compute()
rs_lcdm = cosmo_lcdm.rs_drag()

# ==========================================
# 2. 吉村 A10 ハイブリッド (H0=73.1) の計算
# ==========================================
cosmo_a10 = Class()
params_a10 = {
    'h': 0.731, 'omega_b': 0.02237, 'omega_cdm': 0.1200,
    'A_s': 2.1e-9, 'n_s': 0.965, 'tau_reio': 0.054,
    'has_unified_a10': 'yes',
    'ua10_f_ax': 0.22, 'ua10_phi_trigger': 0.5,
    'has_ua10_tx': 'yes',
    'ua10_tx_omega0': 0.042, 'ua10_tx_zt': 0.035,
    'ua10_tx_sigma': 0.04, 'ua10_tx_dw': -0.60
}
cosmo_a10.set(params_a10)
cosmo_a10.compute()
rs_a10 = cosmo_a10.rs_drag()

# ==========================================
# 3. 残差 (Residual) の計算と出力
# ==========================================
print(f"{'z':<5} | {'H(z) Diff':<10} | {'D_M/rd Diff':<12} | {'D_H/rd Diff':<12}")
print("-" * 45)

for z in z_arr:
    # LCDMの計算
    Hz_lcdm = cosmo_lcdm.Hubble(z)
    DM_lcdm = cosmo_lcdm.angular_distance(z) * (1.+z)
    DH_lcdm = 1. / Hz_lcdm
    
    # A10の計算
    Hz_a10 = cosmo_a10.Hubble(z)
    DM_a10 = cosmo_a10.angular_distance(z) * (1.+z)
    DH_a10 = 1. / Hz_a10
    
    # 差分（パーセント）を計算
    diff_Hz = (Hz_a10 / Hz_lcdm - 1.0) * 100
    diff_DM_rd = ((DM_a10/rs_a10) / (DM_lcdm/rs_lcdm) - 1.0) * 100
    diff_DH_rd = ((DH_a10/rs_a10) / (DH_lcdm/rs_lcdm) - 1.0) * 100
    
    # z=0.01, 0.1, 0.5, 1.0, 2.0 付近だけピックアップして表示
    if abs(z - 0.01) < 0.03 or abs(z - 0.11) < 0.03 or abs(z - 0.51) < 0.03 or abs(z - 1.02) < 0.03 or abs(z - 2.04) < 0.03:
        print(f"{z:.2f}  | {diff_Hz:>+8.2f}%  | {diff_DM_rd:>+10.2f}% | {diff_DH_rd:>+10.2f}%")

cosmo_lcdm.struct_cleanup()
cosmo_lcdm.empty()
cosmo_a10.struct_cleanup()
cosmo_a10.empty()