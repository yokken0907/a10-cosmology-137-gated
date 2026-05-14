import sys
import os
from getdist import mcsamples

# チェーンの読み込み（パスに注意）
chain_root = 'chains/a10_prod_run'

if not os.path.exists(chain_root + '.1.txt'):
    print(f"Error: {chain_root}.1.txt が見当たりません。")
    sys.exit()

# サンプルをロード（最初の30%をburn-inとして捨てる設定）
samples = mcsamples.loadMCSamples(chain_root, settings={'ignore_rows':0.3})

# 統計情報を取得して表示
stats = samples.getMargeStats()
param = stats.parWithName('A10_amplitude')

print("\n--- 解析結果 ---")
print(f"A10_amplitude の平均値: {param.mean}")
print(f"1-sigma 誤差: {param.err}")
print("---------------")