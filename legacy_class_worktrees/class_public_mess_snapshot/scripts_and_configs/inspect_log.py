#!/usr/bin/env python3
from pathlib import Path
import sys

# コマンドライン引数からファイル名を取得
path = Path(sys.argv[1])
text = path.read_text(errors="ignore")

keywords = [
    "H0", "theta_s", "reio", "z_reio", "z_rec", "z_d",
    "sound horizon", "drag", "recombination"
]

print(f"=== Inspecting: {path.name} ===")
for line in text.splitlines():
    low = line.lower()
    if any(k.lower() in low for k in keywords):
        print(line.strip())