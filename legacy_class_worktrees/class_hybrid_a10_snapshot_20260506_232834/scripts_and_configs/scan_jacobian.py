from classy import Class
import numpy as np

# 1. 基準となる標準理論 (Lambda-CDM)
cosmo_lcdm = Class()
params_lcdm = {
    'h': 0.674, 'omega_b': 0.02237, 'omega_cdm': 0.1200,
    'A_s': 2.1e-9, 'n_s': 0.965, 'tau_reio': 0.054
}
cosmo_lcdm.set(params_lcdm)
cosmo_lcdm.compute()
rs_lcdm = cosmo_lcdm.rs_drag()
H0_lcdm = cosmo_lcdm.h() * 100.

# 2. 関数：暗黒物質(ocdm)も調整できるように改良
def get_residuals(f_ax, tx_w0, tx_zt, tx_sig, tx_dw, h_val=0.731, ocdm=0.1200):
    cosmo = Class()
    cosmo.set({
        'h': h_val, 'omega_b': 0.02237, 'omega_cdm': ocdm,  # ← ここが重要！
        'A_s': 2.1e-9, 'n_s': 0.965, 'tau_reio': 0.054,
        'has_unified_a10': 'yes', 'ua10_f_ax': f_ax, 'ua10_phi_trigger': 0.5,
        'has_ua10_tx': 'yes', 'ua10_tx_omega0': tx_w0, 'ua10_tx_zt': tx_zt,
        'ua10_tx_sigma': tx_sig, 'ua10_tx_dw': tx_dw
    })
    cosmo.compute()
    rs = cosmo.rs_drag()
    H0 = cosmo.h() * 100.
    
    z_list = [0.01, 0.52, 1.03, 2.04]
    res = {'rs_ratio': rs / rs_lcdm, 'z': [], 'E_diff': [], 'DM_diff': [], 'DH_diff': []}
    
    for z in z_list:
        Ez_lcdm = cosmo_lcdm.Hubble(z) / H0_lcdm
        DM_lcdm = cosmo_lcdm.angular_distance(z) * (1.+z)
        DH_lcdm = 1. / cosmo_lcdm.Hubble(z)
        
        Ez_mod = cosmo.Hubble(z) / H0
        DM_mod = cosmo.angular_distance(z) * (1.+z)
        DH_mod = 1. / cosmo.Hubble(z)
        
        res['z'].append(z)
        res['E_diff'].append( (Ez_mod/Ez_lcdm - 1.) * 100 )
        res['DM_diff'].append( (DM_mod/DM_lcdm - 1.) * 100 )
        res['DH_diff'].append( (DH_mod/DH_lcdm - 1.) * 100 )
        
    cosmo.struct_cleanup()
    cosmo.empty()
    return res

print("--- A10 ハイブリッド：真の物理的補償スキャン ---")

# 【大本命】 暗黒物質を増やし(0.1400)、H0を72.4でキープ。
# 暗黒物質が増えるとrsが自然に縮むので、A10(f_ax)は少し控えめの 0.12 に設定！
res_mod1 = get_residuals(0.12, 0.042, 0.10, 0.08, -0.40, h_val=0.724, ocdm=0.1400)
print(f"\n[Test 1] 暗黒物質増強版 (ocdm=0.1400, f_ax=0.12) | rs/rs_LCDM = {res_mod1['rs_ratio']:.4f}")
print(" z    | E(z) Diff | D_M (純粋距離) Diff | D_H (純粋距離) Diff")
for i, z in enumerate(res_mod1['z']):
    print(f"{z:<4.2f} | {res_mod1['E_diff'][i]:>+8.2f}% | {res_mod1['DM_diff'][i]:>+17.2f}% | {res_mod1['DH_diff'][i]:>+17.2f}%")

cosmo_lcdm.struct_cleanup()
cosmo_lcdm.empty()