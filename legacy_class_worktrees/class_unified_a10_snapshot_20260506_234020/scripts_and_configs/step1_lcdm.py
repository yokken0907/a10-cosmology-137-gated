import numpy as np
from classy import Class

lcdm = Class()
lcdm.set({
    'H0': 67.4, 'omega_b': 0.0224, 'omega_cdm': 0.120,
    'tau_reio': 0.054, 'A_s': 2.1e-9, 'n_s': 0.965,
    'output': 'tCl', 'l_max_scalars': 2500
})
lcdm.compute()
cl = lcdm.raw_cl(2500)
# データをファイルに保存
np.savez("lcdm_data.npz", ell=cl['ell'], tt=cl['tt'])
print("✅ LCDMのデータを 'lcdm_data.npz' に保存しました。")
lcdm.struct_cleanup(); lcdm.empty()