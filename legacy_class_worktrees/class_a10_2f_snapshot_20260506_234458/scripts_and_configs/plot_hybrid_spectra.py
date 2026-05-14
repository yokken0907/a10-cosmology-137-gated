import matplotlib.pyplot as plt
import numpy as np
from classy import Class

# 共通パラメータ
common_params = {
    'h': 0.674,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'A_s': 2.1e-9,
    'n_s': 0.965,
    'tau_reio': 0.054,
    'output': 'tCl, mPk',
    'l_max_scalars': 2500,
    'P_k_max_1/Mpc': 1.0,
    'YHe': 'BBN'
}

# 1. 基準となる Lambda-CDM モデル
lcdm = Class()
lcdm.set(common_params)
lcdm.compute()

# 2. A10 + Factor X (UA10TX) ハイブリッドモデル
# ※注意: A10を使用するため、必ず newtonian ゲージを指定します。
hybrid_params = common_params.copy()
hybrid_params.update({
    'gauge': 'newtonian',
    'has_unified_a10': 'yes',
    'ua10_f_ax': 0.12,
    'ua10_phi_trigger': 0.5,
    'Omega_fld': 0.042,           # 暗黒エネルギーの一部を流体として扱う
    'fluid_equation_of_state': 'ua10tx',
    'ua10_tx_zt': 0.10,           # 遷移開始の赤方偏移
    'ua10_tx_sigma': 0.04,        # 遷移の期間（幅）
    'ua10_tx_dw': -0.40,          # 状態方程式の変化量
    'use_ppf': 'no',              # PPF近似は使用しない
    'cs2_fld': 1.0                # 音速を光速に固定し発散を抑制
})

hybrid = Class()
hybrid.set(hybrid_params)
hybrid.compute()

# スペクトルデータの取得
cl_lcdm = lcdm.raw_cl(2500)
cl_hybrid = hybrid.raw_cl(2500)

l = cl_lcdm['ell'][2:]
tt_lcdm = (l * (l + 1) * cl_lcdm['tt'][2:]) / (2 * np.pi)
tt_hybrid = (l * (l + 1) * cl_hybrid['tt'][2:]) / (2 * np.pi)

k = np.logspace(-4, 0, 500)
pk_lcdm = np.array([lcdm.pk(ki, 0) for ki in k])
pk_hybrid = np.array([hybrid.pk(ki, 0) for ki in k])

# 描画設定
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# --- CMB TT スペクトル ---
axes[0].plot(l, tt_lcdm, 'k-', label='Lambda-CDM')
axes[0].plot(l, tt_hybrid, 'r--', label='Hybrid A10 + UA10TX')
axes[0].set_xlabel('Multipole l', fontsize=14)
axes[0].set_ylabel('l(l+1)C_l^TT / 2pi', fontsize=14)
axes[0].set_title('CMB Temperature Anisotropy', fontsize=16)
axes[0].set_xlim([2, 2500])
axes[0].legend(fontsize=12)
axes[0].grid(True, linestyle=':', alpha=0.7)

# --- 物質パワースペクトル P(k) ---
axes[1].loglog(k, pk_lcdm, 'k-', label='Lambda-CDM')
axes[1].loglog(k, pk_hybrid, 'r--', label='Hybrid A10 + UA10TX')
axes[1].set_xlabel('k [h/Mpc]', fontsize=14)
axes[1].set_ylabel('P(k) [(Mpc/h)^3]', fontsize=14)
axes[1].set_title('Matter Power Spectrum at z=0', fontsize=16)
axes[1].legend(fontsize=12)
axes[1].grid(True, linestyle=':', alpha=0.7)

plt.tight_layout()
plt.savefig('hybrid_spectra_comparison.png', dpi=300)
print("プロットの生成が完了し、'hybrid_spectra_comparison.png' として保存されました。")

# メモリの解放
lcdm.struct_cleanup()
lcdm.empty()
hybrid.struct_cleanup()
hybrid.empty()