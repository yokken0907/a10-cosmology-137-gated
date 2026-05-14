# WSL最上層 loose files assessment

## 結論

WSLホーム直下に散らばっているファイルは、容量としては大きくない。  
ただし、心理的な散らかり感の原因になっている。

確認されたtop-level file count: 48  
Python loose files: 34  
Archive loose files: 4

## 主なPython loose files

多くは以下の系統である。

- `ucf_alpha_*`
- `e8_ucf_alpha_*`
- `e8_*`
- `samd_*`
- `erbft_*`
- `golden_point_search.py`
- `unified_137_solver.py`

これはA10理論の超初期・基礎数理・137探索・E8/UCF-alpha探索の痕跡と見てよい。

## 推奨扱い

削除ではなく、まず以下へ移動する。

```bash
mkdir -p ~/a10_legacy_frozen/root_loose_files_20260506
mv ~/*.py ~/a10_legacy_frozen/root_loose_files_20260506/ 2>/dev/null
mv ~/all_code*.txt ~/a10_legacy_frozen/root_loose_files_20260506/ 2>/dev/null
```

ただし、`.bashrc`, `.bash_history`, snapshot tar.gz は別扱い。

## 注意

過去に最上層のPythonを消してプログラムが起動しなくなったとのことなので、削除はしない。  
まず「移動して、必要なら戻せる」形にする。

## 容量面

最上層loose filesの容量は、巨大CLASS/BHフォルダに比べれば小さい。  
容量削減の本命は、`class_hybrid_a10`, `class_unified_a10`, `a10_blackhole`, `.cache`, venv類である。
