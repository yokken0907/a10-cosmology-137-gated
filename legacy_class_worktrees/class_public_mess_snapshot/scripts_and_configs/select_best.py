#!/usr/bin/env python3
import csv
import math
from pathlib import Path

CSV_IN = Path("outputs/dneff_grid_summary.csv")
OUT_TXT = Path("outputs/dneff_best.txt")

# A10 Run-G のターゲット値
A10_TARGET = {
    "H0": 72.0,
    "100theta_s": 1.041098,
    "z_reio": 7.66
}

# 許容するズレの重み
SIGMA = {
    "H0": 0.3,
    "100theta_s": 0.0005,
    "z_reio": 0.5
}

def proxy_score(row):
    score = 0.0
    for key in A10_TARGET:
        try:
            val = float(row[key])
            if math.isnan(val): return math.inf
            score += ((val - A10_TARGET[key]) / SIGMA[key]) ** 2
        except:
            return math.inf
    return score

def main():
    with CSV_IN.open() as f:
        rows = list(csv.DictReader(f))
    
    for row in rows:
        row["score"] = proxy_score(row)
    
    # スコアが小さい順にソート
    rows.sort(key=lambda r: r["score"])
    best = rows[0]
    
    lines = [
        "=== Best ΔN_eff-equivalent run ===",
        f"run = {best['run']}",
        f"score = {best['score']:.4f}",
        f"N_eff = {best['N_eff']}",
        f"H0 = {best['H0']}",
        f"100theta_s = {best['100theta_s']}",
        f"z_reio = {best['z_reio']}",
        f"z_d = {best.get('z_d', 'NaN')}"
    ]
    
    OUT_TXT.write_text("\n".join(lines))
    print("\n".join(lines))

if __name__ == "__main__":
    main()