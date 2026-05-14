from classy import Class

# 共通のベースパラメータ
base_params = {
    'h': 0.724, 
    'omega_b': 0.02237, 
    'omega_cdm': 0.1400,
    'A_s': 2.1e-9, 
    'n_s': 0.965, 
    'tau_reio': 0.054,
    'output': 'tCl,pCl,lCl,mPk',
    'l_max_scalars': 2500,
    'P_k_max_1/Mpc': 1.0,
}

def run_test(test_name, extra_params):
    print(f"--- 実行中: {test_name} ---")
    cosmo = Class()
    params = base_params.copy()
    params.update(extra_params)
    try:
        cosmo.set(params)
        cosmo.compute()
        print(f"✅ {test_name}: 正常クリア！")
    except Exception as e:
        print(f"❌ {test_name}: エラーまたはクラッシュ！\n詳細: {e}")
    
    cosmo.struct_cleanup()
    cosmo.empty()
    print("-" * 40)

# 【容疑者A】 A10 初期ブーストのみON
params_a10_only = {
    'has_unified_a10': 'yes',
    'ua10_f_ax': 0.12, 
    'ua10_phi_trigger': 0.5,
}

# 【容疑者B】 Factor X (UA10TX) のみON
params_tx_only = {
    'Omega_fld': 0.042,
    'fluid_equation_of_state': 'ua10tx',
    'ua10_tx_zt': 0.10,
    'ua10_tx_sigma': 0.04,
    'ua10_tx_dw': -0.40,
    'use_ppf': 'no',
    'cs2_fld': 1.0,
}

# 順番にテストを実行
run_test("容疑者A: A10 初期ブースト単独テスト", params_a10_only)
run_test("容疑者B: Factor X (UA10TX) 単独テスト", params_tx_only)