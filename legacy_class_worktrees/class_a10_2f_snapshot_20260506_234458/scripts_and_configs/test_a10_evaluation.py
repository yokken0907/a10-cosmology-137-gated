import numpy as np
from classy import Class

def evaluate_a10_model():
    params = {
        'output': 'tCl, pCl, lCl, mPk',
        'l_max_scalars': 2500,
        'P_k_max_1/Mpc': 3.0,
        
        # 標準宇宙論パラメータ
        'h': 0.6736,
        'omega_b': 0.02237,
        'omega_cdm': 0.1200,
        'A_s': 2.1e-9,
        'n_s': 0.9649,
        'tau_reio': 0.0544,
        
        # 条件分岐 (has_fld == _TRUE_) を満たすためのパラメータ
        'Omega_fld': 1e-5,
        
        # A10-2F-EF 拡張パラメータ
        'has_a10_2f': 'yes',
        'a10_fede_peak': 0.1,
        'a10_log10zc': 3.52,
        'a10_dlogatrig': 0.1,
        'a10_npost': 2.0,
        'a10_xi137': 137.036,
        'a10_gamma0': 0.0,
        'a10_cs_model': 1
    }

    print("Initializing CLASS with A10-2F-EF parameters...")
    cosmo = Class()
    cosmo.set(params)

    try:
        cosmo.compute()
        print("SUCCESS: The compute() function finished without errors.")
        cls = cosmo.lensed_cl(2500)
        tt = cls['tt'][2] * 2 * 3 * 1e12 / (2 * np.pi)
        print(f"Validation Output -> C_l^TT (l=2) = {tt:.4e} [muK^2]")
    except Exception as e:
        print("FAILED: A numerical or theoretical error occurred.")
        print(e)
    finally:
        cosmo.struct_cleanup()
        cosmo.empty()

if __name__ == '__main__':
    evaluate_a10_model()