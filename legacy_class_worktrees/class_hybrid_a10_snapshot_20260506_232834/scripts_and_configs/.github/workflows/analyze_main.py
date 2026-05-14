import sys
import os
from getdist import plots, MCSamples, loadMCSamples
import matplotlib.pyplot as plt

# チェーンのパスを指定
# ./chains/ フォルダ内の a10_phase4_shoes を読み込みます
chain_name = './chains/a10_phase4_shoes'

print("データを読み込み中... 数十万行あるので少し時間がかかります。")
samples = loadMCSamples(chain_name, settings={'ignore_rows': 0.3}) # 最初の30%をバーンインとして捨てる

# 抽出するパラメーターのリスト
# 理論の急所となるパラメーターを絞り込みます
params_to_plot = ['H0', 'omega_cdm', 'n_s', 'ua10_V0', 'ua10_phi_trigger']

# 三角プロット（等高線図）の作成
g = plots.get_subplot_plotter()
g.settings.num_plot_contours = 2 # 68% と 95% の信頼区間を表示
g.triangle_plot(samples, params_to_plot, 
                filled=True, 
                title_limit=1, # 図の上に各パラメーターの値を表示
                legend_labels=['A10 Phase4 shoes'])

# 保存
output_file = 'main_result_triangle.png'
plt.savefig(output_file)
print(f"解析完了！画像ファイル '{output_file}' を出力しました。")