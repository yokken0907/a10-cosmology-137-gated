import re
from classy import Class
import numpy as np

def run_dynamic_test():
    # 1. input.c のソースコードから要求されるパラメータ名と型を抽出
    with open('source/input.c', 'r') as f:
        content = f.read()

    matches1 = re.findall(r'class_read_([a-zA-Z_]+)\s*\(\s*"([^"]+)"', content)
    matches2 = re.findall(r'parser_read_([a-zA-Z_]+)\s*\([^,]+,\s*"([^"]+)"', content)
    
    a10_params = {}
    for dtype, key in (matches1 + matches2):
        if 'a10' not in key.lower(): 
            continue
            
        kl = key.lower()
        # 読み込み型（int/double/string）に厳密に適合する値を設定
        if 'has' in kl:
            a10_params[key] = 'yes' if 'string' in dtype else 1
        elif 'cs' in kl or 'model' in kl:
            a10_params[key] = 1
        elif 'fede' in kl: a10_params[key] = 0.1
        elif 'ac' in kl: a10_params[key] = 0.0003
        elif 'dlog' in kl: a10_params[key] = 0.1
        elif 'wn' in kl: a10_params[key] = 1.0
        elif 'gamma' in kl: a10_params[key] = 0.0
        elif 'xi' in kl: a10_params[key] = 137.036
        elif 'npost' in kl: a10_params[key] = 2.0
        else: a10_params[key] = 1.0

    print("Detected expected A10 parameters from C code:")
    for k, v in a10_params.items():
        print(f"  {k}: {v}")

    if not a10_params:
        print("\nWARNING: No A10 parsing logic found in input.c. The C parser will ignore A10 parameters.")

    # 2. 標準宇宙論パラメータと結合
    params = {
        'output': 'tCl, pCl, lCl, mPk',
        'l_max_scalars': 2500,
        'P_k_max_1/Mpc': 3.0,
        'h': 0.6736,
        'omega_b': 0.02237,
        'omega_cdm': 0.1200,
        'A_s': 2.1e-9,
        'n_s': 0.9649,
        'tau_reio': 0.0544,
    }
    params.update(a10_params)

    # 3. 演算プロセスの実行
    print("\nInitializing CLASS...")
    cosmo = Class()
    cosmo.set(params)

    try:
        cosmo.compute()
        print("\nSUCCESS: compute() finished without errors.")
        cls = cosmo.lensed_cl(2500)
        tt = cls['tt'][2] * 2 * 3 * 1e12 / (2 * np.pi)
        print(f"Validation Output -> C_l^TT (l=2) = {tt:.4e} [muK^2]")
    except Exception as e:
        print("\nFAILED: A numerical or theoretical error occurred during compute().")
        print(e)
    finally:
        cosmo.struct_cleanup()
        cosmo.empty()

if __name__ == '__main__':
    run_dynamic_test()
