import numpy as np
from classy import Class

params = {
    'output': 'tCl, pCl, lCl, mPk',
    'l_max_scalars': 2500,
    'lensing': 'yes',
    'non_linear': 'hmcode',
    
    # 宇宙論パラメータ (MCMCが使おうとした値)
    'h': 0.6736,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'A_s': 1e-10 * np.exp(3.044),
    'n_s': 0.9649,
    'tau_reio': 0.0544,
    
    # Planck の要求設定
    'N_ur': 2.0328,
    'N_ncdm': 1,
    'm_ncdm': 0.06,
    'T_ncdm': 0.71611,
    
    # A10パラメータ
    'has_a10_2f': 'yes',
    'Omega_fld': 1e-5,  # MCMCログに残っていたので念のため再付与
    'a10_fede_peak': 0.1,
    'a10_log10zc': 3.52,
    'a10_dlogatrig': 0.1,
    'a10_npost': 2.0,
    'a10_xi137': 137.036,
    'a10_gamma0': 0.0,
    'a10_cs_model': 1,
    
    # デバッグ用にCLASSの内部出力を詳細化
    'background_verbose': 2,
    'perturbations_verbose': 2,
    'thermodynamics_verbose': 2
}

print("Running CLASS with detailed verbose output...")
cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    print("\nSUCCESS: compute() finished without C-level errors.")
    
    # 派生パラメータのチェック (ここで NaN が出ている可能性大)
    derived = cosmo.get_current_derived_parameters(['Omega_Lambda'])
    print(f"Derived Omega_Lambda: {derived['Omega_Lambda']}")
    
except Exception as e:
    print(f"\nCRITICAL ERROR in CLASS:")
    print(e)
finally:
    cosmo.struct_cleanup()
    cosmo.empty()
