import numpy as np
from pathlib import Path

# ファイルパス
STD_BG = Path('output/std_base_00_background.dat')
A10_BG = Path('output/project137_16_background.dat')

# dNeffモデルのファイルを自動検索
def find_bg_file(folder_path):
    folder = Path(folder_path)
    bg_files = list(folder.glob('*background.dat'))
    if not bg_files:
        raise FileNotFoundError(f"😭 {folder_path} の中に background.dat が見つかりません！")
    return bg_files[0]

# CLASSの background.dat は z が降順（大きい順）なので、np.interp用に反転させる
def interp_descending(x_eval, x_arr, y_arr):
    return np.interp(x_eval, x_arr[::-1], y_arr[::-1])

def calc_bao(file_path):
    data = np.loadtxt(file_path)
    # inspect_bg.py で確認した列番号を使用
    z_arr = data[:, 0]
    H_arr = data[:, 3]     # H [1/Mpc]
    DA_arr = data[:, 5]    # ang.diam.dist.
    rs_arr = data[:, 7]    # comov.snd.hrz.
    
    # バリオンドラッグ期 (z ≈ 1060) での音響地平線 r_s を取得
    rs_d = interp_descending(1060.0, z_arr, rs_arr)
    
    results = {}
    # 典型的なBAOの観測赤方偏移 (BOSS銀河サーベイなど)
    for z_target in [0.38, 0.51, 0.61]:
        H = interp_descending(z_target, z_arr, H_arr)
        DA = interp_descending(z_target, z_arr, DA_arr)
        
        # 共動角径距離 D_M = (1+z) * D_A (平坦宇宙の場合)
        DM = (1.0 + z_target) * DA
        
        # BAO指標の計算
        results[f"DM/rs(z={z_target})"] = DM / rs_d
        results[f"H*rs(z={z_target})"]  = H * rs_d
        
    return results

def main():
    try:
        DNEFF_BG = find_bg_file('outputs/dneff_grid/Neff3.20_h0.700/')
    except Exception as e:
        print(e)
        return

    # 各モデルのBAO指標を計算
    a10_res = calc_bao(A10_BG)
    dn_res = calc_bao(DNEFF_BG)
    
    has_std = STD_BG.exists()
    if has_std:
        std_res = calc_bao(STD_BG)
    else:
        print("⚠️ 標準モデルが見つかりません。A10とdNeffのみ比較します。")
        std_res = {k: np.nan for k in a10_res.keys()}

    # 比較表の出力
    print("\n" + "="*85)
    print(f"{'BAO Indicator':<20} | {'Std LCDM (h=0.67)':<18} | {'A10 (H0=72)':<15} | {'A10 Diff (%)':<15}")
    print("-" * 85)
    
    for key in a10_res.keys():
        std_val = std_res[key]
        a10_val = a10_res[key]
        
        if has_std:
            diff_pct = (a10_val - std_val) / std_val * 100
            diff_str = f"{diff_pct:+.2f} %"
            std_str = f"{std_val:.4f}"
        else:
            diff_str = "N/A"
            std_str = "N/A"
            
        print(f"{key:<20} | {std_str:<18} | {a10_val:.4f}{'':<8} | {diff_str:<15}")
    
    print("="*85 + "\n")

if __name__ == "__main__":
    main()