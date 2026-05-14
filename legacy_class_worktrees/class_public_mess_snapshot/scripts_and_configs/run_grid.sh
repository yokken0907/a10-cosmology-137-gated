#!/usr/bin/env bash
set -euo pipefail

CLASS_BIN="./class"
INI_DIR="runs/dneff_grid"
LOG_DIR="outputs/logs"
mkdir -p "$LOG_DIR"

echo "=== グリッド探索を開始します ==="
for ini in "$INI_DIR"/*.ini; do
  base=$(basename "$ini" .ini)
  echo "Running $base ..."
  
  # 実行と同時に、標準出力をログファイルとして保存する（これが重要です）
  "$CLASS_BIN" "$ini" > "$LOG_DIR/${base}.log" 2>&1 || {
    echo "⚠️ 失敗: $base" >&2
    continue
  }
done
echo "=== 探索完了 ==="