from classy import Class
import matplotlib.pyplot as plt
import numpy as np

# 1. 標準モデル (ΛCDM) の計算
lcdm = Class()
lcdm.set({'H0': 67.4, 'Omega_b': 0.0224, 'Omega_cdm': 0.120, 'tau_reio': 0.054, 'output': 'tCl,pCl,lCl'})
lcdm.compute()
cl_lcdm = lcdm.raw_cl(2500)

# 2. 吉村流 A10モデル の計算 (ベストフィット値を入力)
a10 = Class()
# verify_residual.py の修正
# verify_residual.py の a10.set 部分を以下のように書き換えてください
a10.set({
    'H0': 68.531777,
    'omega_b': 0.020029673,      # さっきの1行から抜き出した正確な値
    'omega_cdm': 0.12590406,     # 同上
    'tau_reio': 0.040045122,     # 同上
    'ua10_f_ax': 0.099217841,
    'ua10_V0': 0.026205356,
    'ua10_Gamma0': 0.013718803,
    'output': 'tCl,pCl,lCl'
})
a10.compute()
cl_a10 = a10.raw_cl(2500)

# 3. 残差（差分）の計算とプロット
l = cl_lcdm['ell']
# 温度ゆらぎの差分を表示 (l(l+1)Cl / 2pi 形式)
factor = l * (l + 1) / (2 * np.pi)
residual = (cl_a10['tt'] - cl_lcdm['tt']) * factor

plt.plot(l, residual)
plt.title("Residual: A10 Model vs Standard Lambda-CDM")
plt.xlabel("Multipole moment (l)")
plt.ylabel("Delta Dl_TT [uK^2]")
plt.grid(True)
plt.savefig("residual_plot.png")