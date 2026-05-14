#!/usr/bin/env python3
from pathlib import Path
import re
import sys

# コマンドライン引数からファイル名を取得
path = Path(sys.argv[1])

mapping = {}
with path.open() as f:
    for line in f:
        if not line.startswith("#"):
            break
        # "# 1:z  2:proper time" のような行から列番号と名前を抽出
        parts = re.findall(r"(\d+)\s*:\s*([^\t#]+)", line)
        for idx_str, name in parts:
            mapping[int(idx_str) - 1] = name.strip()

print(f"=== Columns in {path.name} ===")
for idx in sorted(mapping):
    print(f"Column {idx} -> {mapping[idx]}")