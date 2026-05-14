import numpy as np
from classy import Class

def test_a10_model():
    # 1. A10-2F-EF理論の検証用パラメータセット
    params = {
        'output': 'tCl, pCl, lCl, mPk',
        'l_max_scalars': 2500,
        'P_k_max_1/Mpc': 3.0,
        
        # 標準宇宙論パラメータ (Planck 2018 base)
        'h': 0.6736,
        'omega_b': 0.02237,
        'omega_cdm': 0.1200,
        'A_s': 2.1e-9,
        'n_s': 0.9649,
        'tau_reio': 0.0544,
        
        # A10-2F-EF 拡張パラメータ
        'has_a10_2f': 'yes',
        'a10_fede_peak': 0.1,    # 暗黒エネルギー密度のピーク割合 (f_EDE)
        'a10_ac': 0.0003,        # トリガーとなるスケール因子 (a_c)
        'a10_dlogatrig': 0.1,    # 相転移の幅
        'a10_wn': 1.0,           # 状態方程式パラメータ (n)
        'a10_gamma0': 0.0,       # 相互作用の強さ (まずは0で安全性を検証)
        'a10_xi137': 137.036,    # 微細構造定数パラメータ
        'a10_npost': 2.0,
        'a10_cs_model': 1        # 有効音速モデル (1 = c_s^2 = w_n)
    }

    print("Initialize CLASS with A10-2F-EF model...")
    cosmo = Class()
    cosmo.set(params)

    try:
        # 2. 微分方程式系の積分およびスペクトル演算
        cosmo.compute()
        print("SUCCESS: The compute() function finished without errors.")

        # 3. CMBスペクトルの取得検証
        cls = cosmo.lensed_cl(2500)
        ell = cls['ell'][2:]
        tt = cls['tt'][2:] * ell * (ell + 1) * 1e12 / (2 * np.pi)
        print(f"Validation Output -> C_l^TT (l=2) = {tt[0]:.4e} [muK^2]")

    except Exception as e:
        print("FAILED: A numerical or theoretical error occurred during compute().")
        print(e)
    finally:
        # 4. メモリアロケーションの解放
        cosmo.struct_cleanup()
        cosmo.empty()

if __name__ == '__main__':
    test_a10_model()