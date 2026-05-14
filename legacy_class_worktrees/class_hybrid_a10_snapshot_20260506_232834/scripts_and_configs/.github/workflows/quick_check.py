import matplotlib.pyplot as plt
from getdist import loadMCSamples, plots

# データの読み込み
samples = loadMCSamples('./chains_h0_scan/scan_730_unlimit', settings={'ignore_rows': 0.3})

# 山の形（1D分布）と相関（2D）を同時に確認
g = plots.get_subplot_plotter()
g.triangle_plot(samples, ['ua10_V0', 'ua10_phi_trigger', 'omega_cdm'], 
                filled=True, 
                title_limit=1)

plt.savefig('quick_730_check.png')
print("画像 'quick_730_check.png' を作成しました。")