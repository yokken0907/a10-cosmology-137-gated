import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
import os

# 視覚的設定
plt.style.use('dark_background')
colors = {0.0: 'gray', 1.0: 'springgreen', 2.0: 'fuchsia'}
k_values = [0.0, 1.0, 2.0]
ini_file = 'a10_test_ver2.ini'
output_dir = 'output/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

fig, ax = plt.subplots(figsize=(10, 7))

for k in k_values:
    print(f"--- k = {k} で CLASS を実行中 ---")
    
    # 1. .ini ファイルの書き換え
    with open(ini_file, 'r') as f:
        content = f.read()
    
    # rbh_coupling_k の行を置換
    content = re.sub(r'rbh_coupling_k = .*', f'rbh_coupling_k = {k}', content)
    # root 名を k ごとに固定して出力が混ざらないようにする
    content = re.sub(r'root = .*', f'root = {output_dir}k_{k}_', content)
    
    with open('tmp_k_run.ini', 'w') as f:
        f.write(content)
    
    # 2. CLASS の実行
    subprocess.run(['./class', 'tmp_k_run.ini'], capture_output=True)
    
    # 3. 生成されたデータの読み込み
    data_path = f'{output_dir}k_{k}_background.dat'
    if os.path.exists(data_path):
        data = np.loadtxt(data_path)
        z = data[:, 0]
        H = data[:, 3]
        
        # z < 3 の範囲に絞ってプロット
        mask = (z >= 0) & (z <= 3)
        ax.plot(z[mask], H[mask], label=f'k = {k}', color=colors[k], linewidth=2)
    else:
        print(f"警告: {data_path} が生成されませんでした。")

# グラフの仕上げ
ax.set_xlabel('Redshift $z$', fontsize=12)
ax.set_ylabel('$H(z)$ [1/Mpc]', fontsize=12)
ax.set_title('Sensitivity Analysis: Effect of RBH Coupling $k$ on $H(z)$', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(title="Coupling Constant $k$")

plt.savefig('a10_k_comparison.png')
print("\n比較グラフを保存しました: a10_k_comparison.png")