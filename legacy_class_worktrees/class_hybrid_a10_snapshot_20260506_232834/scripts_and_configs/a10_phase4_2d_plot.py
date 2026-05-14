# corner_plot.py として保存して実行
import matplotlib.pyplot as plt
from getdist import plots, MCSamples
import numpy as np

# データの読み込み（ chains フォルダ内の最終データを使用）
data = np.loadtxt('chains/a10_phase4_shoes.1.txt')
# 重み、対数尤度を除いたパラメータ部分を抽出
# Col 2: H0, Col 11: alpha_inv
samples_data = data[:, [2, 11]] 
names = ['H0', 'alpha_inv']
labels = [r'H_0', r'\alpha^{-1}']

samples = MCSamples(samples=samples_data, names=names, labels=labels)

# プロットの作成
g = plots.get_subplot_plotter()
g.triangle_plot(samples, filled=True, colors=['#006fed'])
plt.savefig("a10_correlation.png")
print("プロット完了: a10_correlation.png を確認してください。")