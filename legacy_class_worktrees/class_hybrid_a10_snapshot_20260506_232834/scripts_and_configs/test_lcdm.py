from classy import Class

cosmo = Class()
params = {
    'h': 0.674,
    'omega_b': 0.02237,
    'omega_cdm': 0.1200,
    'A_s': 2.1e-9,
    'n_s': 0.965,
    'tau_reio': 0.054,
    'output': 'tCl'
}

print("--- 基準テスト：Lambda-CDM ---")
try:
    cosmo.set(params)
    cosmo.compute()
    print("正常に計算が完了しました。")
except Exception as e:
    print("エラー発生:", e)

cosmo.struct_cleanup()
cosmo.empty()