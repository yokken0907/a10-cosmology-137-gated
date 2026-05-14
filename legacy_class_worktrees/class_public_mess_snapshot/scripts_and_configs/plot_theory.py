import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# プロット環境の設定
plt.style.use('dark_background')
plt.rcParams.update({
    'font.size': 14,
    'lines.linewidth': 2.5,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.facecolor': '#121212',
    'axes.facecolor': '#121212'
})

def load_class_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    headers = []
    for line in lines:
        if line.startswith('#'):
            if 'z' in line or 'l' in line:
                # 余分な文字を削除してヘッダーリストを作成
                clean_line = line.replace('#', '').strip()
                headers = [h.strip() for h in clean_line.split()]
        else:
            break
            
    data = np.loadtxt(filename)
    df = pd.DataFrame(data, columns=headers if len(headers) == data.shape[1] else [f"col_{i}" for i in range(data.shape[1])])
    return df

bg_file = 'output/project137_00_background.dat'
cl_file = 'output/project137_00_cl.dat'

# 1. 背景進化のプロット
try:
    df_bg = load_class_data(bg_file)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 該当するカラム名を検索
    z_col = [c for c in df_bg.columns if 'z' in c][0]
    rho_y_cols = [c for c in df_bg.columns if 'rho_Y' in c]
    rho_x_cols = [c for c in df_bg.columns if 'rho_X' in c]
    
    if rho_y_cols and rho_x_cols:
        ax.plot(df_bg[z_col], df_bg[rho_y_cols[0]], label='Parent Fluid (rho_Y)', color='#00ffcc')
        ax.plot(df_bg[z_col], df_bg[rho_x_cols[0]], label='Daughter Fluid (rho_X)', color='#ff3366')
        
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlim(1e5, 1)  # 過去(高赤方偏移)から現在(z=0)へ
        ax.set_xlabel('Redshift z')
        ax.set_ylabel('Energy Density')
        ax.set_title('137-Stability-Gated A10 Model: Background')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        bg_out = 'output/plot_background.png'
        plt.savefig(bg_out)
        print(f"背景進化のプロットを {bg_out} に保存しました。")
    else:
        print("エラー: 背景データ内に rho_Y または rho_X のカラムが見つかりません。")
except Exception as e:
    print(f"背景データの処理中にエラーが発生しました: {e}")

# 2. CMB温度揺らぎパワースペクトルのプロット
try:
    if os.path.exists(cl_file):
        df_cl = load_class_data(cl_file)
        fig, ax = plt.subplots(figsize=(10, 6))
        
        l_col = [c for c in df_cl.columns if 'l' in c.lower()][0]
        tt_cols = [c for c in df_cl.columns if 'tt' in c.lower() or 'TT' in c]
        
        if tt_cols:
            ax.plot(df_cl[l_col], df_cl[tt_cols[0]], label='CMB TT Spectrum', color='#ffcc00')
            ax.set_xlim(2, 2500)
            ax.set_xlabel('Multipole l')
            ax.set_ylabel('l(l+1)Cl / 2pi')
            ax.set_title('137-Stability-Gated A10 Model: CMB TT')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            cl_out = 'output/plot_cl.png'
            plt.savefig(cl_out)
            print(f"CMBスペクトルのプロットを {cl_out} に保存しました。")
        else:
            print("エラー: CMBデータ内に TT のカラムが見つかりません。")
    else:
        print(f"{cl_file} が存在しません。")
except Exception as e:
    print(f"CMBデータの処理中にエラーが発生しました: {e}")