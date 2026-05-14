import matplotlib.pyplot as plt
import numpy as np
from classy import Class

print("🔬 最終診断：A10 + Massive Neutrino の CMB Ratio を確認します...")

# --- 1. 基準となる LCDM ---
lcdm = Class()
lcdm.set({'H0': 67.4, 'omega_b': 0.0224, 'omega_cdm': 0.120, 'output': 'tCl', 'l_max_scalars': 2500})
lcdm.compute()
cl_l = lcdm.raw_cl(2500)
ell_l = cl_l['ell'][2:]
tt_l = cl_l['tt'][2:]
lcdm.struct_cleanup()
lcdm.empty()

# --- 2. 黄金の Unified A10 + Neutrino (YAMLのref値) ---
a10 = Class()
params_a10 = {
    '100*theta_s': 1.0411, 'omega_b': 0.0224, 'omega_cdm': 0.117,
    'tau_reio': 0.054, 'A_s': 2.1e-9, 'n_s': 0.965,
    'has_unified_a10': 'yes',
    'ua10_phi_trigger': 1e-4, 'ua10_Delta_phi': 0.8, 'ua10_n_ax': 2.5,
    'ua10_f_ax': 0.30, 'ua10_V0': 0.03, 'ua10_Gamma0': 0.005,
    'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': 0.15, 'T_ncdm': 0.71611,
    'output': 'tCl', 'l_max_scalars': 2500
}
a10.set(params_a10)
a10.compute()
cl_a = a10.raw_cl(2500)
tt_a = cl_a['tt'][2:]
a10.struct_cleanup()
a10.empty()

# --- 3. Ratio のプロット ---
limit = min(len(tt_a), len(tt_l))
ratio = tt_a[:limit] / tt_l[:limit]

plt.figure(figsize=(10, 6))
plt.plot(ell_l[:limit], ratio, 'm-', lw=2)
plt.axhline(1.0, color='k', ls='-')
plt.axhline(1.02, color='r', ls='--', label='+2% Limit')
plt.axhline(0.98, color='b', ls='--', label='-2% Limit')
plt.axvspan(1000, 2500, color='gray', alpha=0.1, label='Planck High-l Zone')
plt.ylim(0.95, 1.05)
plt.xlim(2, 2500)
plt.xlabel('Multipole $\ell$')
plt.ylabel('Ratio $C_\ell^{TT} (A10+\\nu) / C_\ell^{TT} (\Lambda CDM)$')
plt.title('CMB Power Spectrum Ratio (A10 + $\sum m_\\nu$)')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("final_cmb_ratio.png", dpi=300)
print("✅ final_cmb_ratio.png を保存しました！ これをPIに見せましょう。")