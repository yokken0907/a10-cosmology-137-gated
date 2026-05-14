#!/usr/bin/env python3
import csv
import re
import math
from pathlib import Path

LOG_DIR = Path("outputs/logs")
CSV_OUT = Path("outputs/dneff_grid_summary.csv")

# ログから抽出するパターン（grepの結果に完全に合わせました！）
PATTERNS = {
    "100theta_s": re.compile(r"100\*theta_s\s*=\s*([0-9Ee+\-.]+)"),
    "z_reio": re.compile(r"reionization at z = ([0-9Ee+\-.]+)"),
    "z_d": re.compile(r"baryon drag stops at z = ([0-9Ee+\-.]+)"),
}

# ファイル名から N_eff と h を抽出するパターン
NAME_PATTERN = re.compile(r"run_Neff([0-9.]+)_h([0-9.]+)")

def parse_log(log_path):
    text = log_path.read_text(errors="ignore")
    row = {"run": log_path.stem}
    
    # 1. ファイル名から確実に取得
    m_name = NAME_PATTERN.search(log_path.stem)
    if m_name:
        row["N_eff"] = float(m_name.group(1))
        row["H0"] = float(m_name.group(2)) * 100.0
    else:
        row["N_eff"], row["H0"] = math.nan, math.nan

    # 2. ログの中身から取得
    for key, pattern in PATTERNS.items():
        m = pattern.search(text)
        row[key] = float(m.group(1)) if m else math.nan
        
    return row

def main():
    rows = []
    for log_path in sorted(LOG_DIR.glob("run_*.log")):
        rows.append(parse_log(log_path))
    
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run", "N_eff", "H0", "100theta_s", "z_reio", "z_d"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ 集計完了: {len(rows)}件のデータを保存しました。")

if __name__ == "__main__":
    main()