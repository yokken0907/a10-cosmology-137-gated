import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from getdist import loadMCSamples
import getdist.plots as gdplt

# Matplotlibの数式レンダラーを完全に無効化
plt.rcParams['text.usetex'] = False

root_path = os.path.abspath('chains/a10_prod_run')

try:
    # 1. チェーンを読み込む
    samples = loadMCSamples(root_path)
    
    # 2. 【ここが重要】データを探すための「名前」はアンダースコアのまま
    #    表示される「ラベル」だけをハイフンに変える
    for p in samples.paramNames.names:
        p.label = p.name.replace('_', '-') 

    # 3. グラフに出すパラメータのリスト（元の名前で指定）
    plot_params = ['H0', 'ua10_f_ax', 'ua10_V0', 'ua10_Gamma0']

    # 4. プロッターの準備
    g = gdplt.get_subplot_plotter()
    
    # 5. プロット実行
    g.triangle_plot(samples, plot_params, filled=True)

    # 6. 保存
    g.export('a10_triangle_plot.png')
    print("✨ ついに、ついに、ついに...成功しました！！")
    print("画像ファイル 'a10_triangle_plot.png' が生成されました。")

except Exception as e:
    print(f"❌ 最後の最後でエラー: {e}")
