import numpy as np
from getdist import loadMCSamples

# チェーンの読み込み
samples = loadMCSamples('chains/a10_main_rescue')

# 最小 chi2 の行を特定
chi2_values = samples.samples[:, samples.index['chi2']]
best_fit_idx = np.argmin(chi2_values)

# 各観測項目の chi2 内訳を取得
liks = [
    'chi2__planck_2018_highl_plik.TTTEEE',
    'chi2__planck_2018_lowl.TT',
    'chi2__planck_2018_lowl.EE',
    'chi2__bao.sdss_dr12_consensus_bao',
    'chi2__sn.pantheonplus'
]

print(f"\n" + "="*60)
print(f"   A10理論：観測データ別不一致（残差）内訳")
print(f"   (Best chi2: {chi2_values[best_fit_idx]:.4f} 地点での解析)")
print("-"*60)

for lik in liks:
    try:
        val = samples.samples[best_fit_idx, samples.index[lik]]
        print(f"   {lik:<40} : {val:>10.4f}")
    except:
        continue

print("="*60 + "\n")