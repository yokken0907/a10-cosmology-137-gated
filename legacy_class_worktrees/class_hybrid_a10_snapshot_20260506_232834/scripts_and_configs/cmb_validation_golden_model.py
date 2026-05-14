import numpy as np
from classy import Class

# --- 監督官の「黄金の数値」をそのまま流し込む ---
params = {
    '100*theta_s': 1.0411,
    'omega_b': 0.0224,
    'omega_cdm': 0.120,
    'tau_reio': 0.054,
    'A_s': 2.1e-9,
    'n_s': 0.965,
    'has_unified_a10': 'yes',
    'ua10_n_ax': 2.5,
    'ua10_f_ax': 0.25,
    'ua10_V0': 2.0e-4,
    'ua10_Gamma0': 0.65,
    'ua10_phi_trigger': 1e-6,
    'ua10_Delta_phi': 0.60,
    
    # 必要最低限。余計な精度パラメータは一切入れない
    'output': 'tCl', 
    'l_max_scalars': 2500
}

a10 = Class()
try:
    print("🔭 黄金モデルの計算を開始（今度は通れ！）...")
    a10.set(params)
    a10.compute() # 🎯 事件現場：ここを突破できるか
    print("✅ 計算成功！グラフ作成に移行します。")
    
    # 成功したら、ここで簡単な数値だけ表示
    print(f"H0: {a10.h()*100:.2f}")

except Exception as e:
    print(f"❌ やはりここで落ちるようです:\n{e}")

# メモリ解放
a10.struct_cleanup()
a10.empty()