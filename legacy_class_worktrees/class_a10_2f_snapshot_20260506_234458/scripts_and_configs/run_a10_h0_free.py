from classy import Class

params = {
    # --- 基本宇宙論（H0を削除し、theta_sを固定！） ---
    '100*theta_s': 1.0411,   # Planckの観測値
    'omega_b': 0.0224,       # 物理密度（Ω_b h^2）
    'omega_cdm': 0.120,      # 物理密度（Ω_c h^2）
    'tau_reio': 0.054,
    'A_s': 2.1e-9,
    'n_s': 0.965,

    # --- 出力と精度 ---
    'output': 'tCl,pCl,lCl,mPk',
    'l_max_scalars': 3000,
    'P_k_max_h/Mpc': 5.0,
    'z_max_pk': 5.0,

    # --- Unified A10（黄金のパラメータ） ---
    'has_unified_a10': 'yes',

    'ua10_n_ax': 2.5,
    'ua10_f_ax': 0.25,

    'ua10_V0': 2.0e-4,
    'ua10_Gamma0': 0.65,

    'ua10_phi_trigger': 1e-6,
    'ua10_Delta_phi': 0.60,

    'background_verbose': 1,
}

# CLASSの初期化と計算
cosmo = Class()
cosmo.set(params)
cosmo.compute()

print("--- Unified A10 最終診断 ---")

# --- H0 の取得 ---
# ※ChatGPTの「Hubble(0) * 2997.92458」は光速の桁(299792.458)を間違えており
# バグる危険があるため、CLASS標準の cosmo.h() を使います。
H0 = cosmo.h() * 100
print(f"H0 = {H0:.2f}")

# --- theta_s の確認 ---
#theta_s = cosmo.theta_s() * 100
#print(f"100*theta_s = {theta_s:.4f} (Input: 1.0411)")

# --- rs_d の取得 ---
rs_d = cosmo.rs_drag()
print(f"rs_d = {rs_d:.2f} Mpc")

# --- S8 の取得 ---
sigma8 = cosmo.sigma8()
Omega_m = cosmo.Omega_m()
S8 = sigma8 * (Omega_m / 0.3)**0.5
print(f"S8 = {S8:.4f}")

# メモリ解放
cosmo.struct_cleanup()
cosmo.empty()