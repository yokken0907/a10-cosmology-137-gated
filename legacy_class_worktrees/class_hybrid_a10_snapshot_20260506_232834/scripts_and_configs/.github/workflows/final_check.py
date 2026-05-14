import numpy as np
import pandas as pd
import glob
import os

# 新しく作ったディレクトリを指定
chain_dir = "./chains_h0_scan/" 
CHI2_COL = 1       # minuslogpost
H0_COL = 2         # Hubble constant
OMEGA_CDM = 4      # omega_cdm
NS_COL = 6         # n_s
A10_COL = 11       # A10 scale (chi)

def scan_victory():
    files = glob.glob(os.path.join(chain_dir, "*.minimum.txt"))
    if not files: 
        print("スキャン結果のファイルが見つかりません。")
        return

    data_list = [pd.read_csv(f, sep='\s+', comment='#', header=None) for f in files]
    df = pd.concat(data_list, ignore_index=True)

    # 見やすくソート
    df = df.sort_values(by=H0_COL)

    print("\n=== A10理論：ウォール・ブレイク(H0=73突破) 最終確認 ===")
    print(f"{'H0':>5} | {'Total Chi2':>10} | {'A10 Scale':>10} | {'n_s':>10} | {'omega_cdm':>10}")
    print("-" * 60)

    for _, row in df.iterrows():
        h0_val = row[H0_COL]
        chi2_val = row[CHI2_COL]
        a10_val = row[A10_COL]
        ns_val = row[NS_COL]
        ocdm_val = row[OMEGA_CDM]
        
        print(f"{h0_val:5.1f} | {chi2_val:10.2f} | {a10_val:10.3f} | {ns_val:10.4f} | {ocdm_val:10.5f}")

if __name__ == "__main__":
    scan_victory()