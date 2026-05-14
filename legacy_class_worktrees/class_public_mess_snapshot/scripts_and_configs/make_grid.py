#!/usr/bin/env python3
from pathlib import Path
import itertools

BASE_INI = Path("dneff_base.ini")
OUT_DIR = Path("runs/dneff_grid")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 探索範囲の設定
neff_vals = [round(x, 2) for x in [3.20 + i*0.05 for i in range(13)]]
h_vals = [round(x, 3) for x in [0.700 + i*0.005 for i in range(7)]]

def main():
    # 改行コード(\r)の混入をここで自動除去する
    template = BASE_INI.read_text(errors="ignore").replace('\r', '')
    count = 0
    
    for neff, h in itertools.product(neff_vals, h_vals):
        tag = f"Neff{neff:.2f}_h{h:.3f}"
        
        # ⚠️ 追加：CLASSが出力するための空フォルダを事前に作ってあげる
        out_folder = Path(f"outputs/dneff_grid/{tag}")
        out_folder.mkdir(parents=True, exist_ok=True)
        
        root_path = f"{out_folder}/"
        
        content = (
            template
            .replace("__NEFF__", f"{neff:.2f}")
            .replace("__H__", f"{h:.3f}")
            .replace("__ROOT__", root_path)
        )
        
        ini_path = OUT_DIR / f"run_{tag}.ini"
        ini_path.write_text(content)
        count += 1

    print(f"✅ 生成完了: {count} 個の .ini ファイルと出力先フォルダを作成しました。")

if __name__ == "__main__":
    main()