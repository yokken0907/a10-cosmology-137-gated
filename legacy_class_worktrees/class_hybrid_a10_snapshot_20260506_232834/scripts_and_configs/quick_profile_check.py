import numpy as np
import pandas as pd
import glob
import os

# --- 解析設定 ---
chain_dir = "./chains/" 
# ログに基づいた正確なインデックス (0始まり)
CHI2_TOTAL = 1     # minuslogpost
H0_COL = 2         # Hubble constant
NS_COL = 6         # n_s
A10_COL = 11       # A10 scale (chi)
OMEGA_CDM = 4      # omega_cdm

def deep_diagnosis():
    files = glob.glob(os.path.join(chain_dir, "*.txt"))
    if not files: return

    data_list = [pd.read_csv(f, sep='\s+', comment='#', header=None) for f in files]
    df = pd.concat(data_list, ignore_index=True)

    # H0の範囲を指定してフィルタリング
    df['h0_bin'] = np.round(df[H0_COL] * 2) / 2
    
    print("\n=== A10理論：境界領域ダイアグノシス報告 ===")
    print(f"{'H0':>5} | {'Total Chi2':>10} | {'A10 (chi)':>10} | {'ns':>10} | {'omega_cdm':>10}")
    print("-" * 65)

    # 安定領域(72.0)と壁の領域(72.5, 73.0)を比較
    for target_h0 in [71.5, 72.0, 72.5, 73.0]:
        subset = df[df['h0_bin'] == target_h0]
        if not subset.empty:
            best_fit = subset.loc[subset[CHI2_TOTAL].idxmin()]
            print(f"{target_h0:5.1f} | {best_fit[CHI2_TOTAL]:10.2f} | {best_fit[A10_COL]:10.2f} | {best_fit[NS_COL]:10.4f} | {best_fit[OMEGA_CDM]:10.5f}")

if __name__ == "__main__":
    deep_diagnosis()