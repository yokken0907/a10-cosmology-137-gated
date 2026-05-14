from classy import Class
import sys

# ベース（共通）設定
base = {
    'h': 0.724, 'omega_b': 0.02237, 'omega_cdm': 0.1400,
    'A_s': 2.1e-9, 'n_s': 0.965, 'tau_reio': 0.054,
    'gauge': 'newtonian',  # ←★追加！CDMが動くA10には必須の測り方！
}

# A10とFactor Xの部品
a10 = {'has_unified_a10': 'yes', 'ua10_f_ax': 0.12, 'ua10_phi_trigger': 0.5}
tx = {'Omega_fld': 0.042, 'fluid_equation_of_state': 'ua10tx', 'ua10_tx_zt': 0.10, 'ua10_tx_sigma': 0.04, 'ua10_tx_dw': -0.40, 'use_ppf': 'no', 'cs2_fld': 1.0}
pert = {'output': 'tCl,pCl,lCl,mPk', 'l_max_scalars': 2500, 'P_k_max_1/Mpc': 1.0}

def run_step(step_name, params_dict):
    print(f"\n--- {step_name} ---")
    sys.stdout.flush() # 画面にすぐ表示させる
    cosmo = Class()
    try:
        cosmo.set(params_dict)
        cosmo.compute()
        print("✅ 成功！")
    except Exception as e:
        print(f"❌ エラー: {e}")
    cosmo.struct_cleanup()
    cosmo.empty()

print("🚨 衝突地点特定チキンレース開始 🚨")

# Step 1: ハイブリッドで背景膨張だけ計算する（揺らぎ無し）
p1 = {**base, **a10, **tx}
run_step("Step 1: ハイブリッド（背景膨張のみ）", p1)

# Step 2: ハイブリッドで揺らぎを計算する（再結合モデルはデフォルト）
p2 = {**base, **a10, **tx, **pert}
run_step("Step 2: ハイブリッド（摂動あり・デフォルト再結合）", p2)

# Step 3: ハイブリッドで揺らぎを計算する（recfast指定）
p3 = {**base, **a10, **tx, **pert, 'recombination': 'recfast'}
run_step("Step 3: ハイブリッド（摂動あり ＋ recfast指定）", p3)

print("\n🎉 すべてのステップを完走しました！")