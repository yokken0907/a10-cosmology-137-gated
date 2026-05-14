import sys
import os
from getdist import loadMCSamples, plots

# カレントディレクトリの絶対パスを取得
current_dir = os.getcwd()
file_root = os.path.join(current_dir, 'test_mcmc_output')

print(f"Searching for files with prefix: {file_root}")

# ファイルの存在確認
if not os.path.exists(file_root + '.1.txt'):
    print(f"Error: Chain file {file_root}.1.txt not found.")
    print("Please make sure you are in the same directory where cobaya is running.")
    sys.exit(1)

try:
    # ignore_rowsを0.1（最初の10%）に下げて、少ないデータでも読み込めるように調整
    samples = loadMCSamples(file_root, settings={'ignore_rows': 0.1})
    print("Samples loaded successfully.")
    
    # プロットの実行
    g = plots.get_subplot_plotter()
    # H0, w0_fld (Delta_0), omega_fld の3つをターゲットにする
    plot_params = ['H0', 'w0_fld', 'omega_fld']
    
    g.triangle_plot(samples, plot_params, filled=True)
    
    output_file = 'tentative_analysis.png'
    g.export(output_file)
    print(f"Successfully saved plot to: {os.path.abspath(output_file)}")

except Exception as e:
    print(f"An error occurred during analysis: {e}")
