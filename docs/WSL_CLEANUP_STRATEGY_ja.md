# WSL整理戦略

## 基本方針

削除ではなく、以下の3層に分ける。

```text
~/a10_rebuild_clean/
  論文別GitHub公開候補、小型snapshot、再構築用作業台

~/a10_legacy_frozen/
  旧巨大フォルダ、旧実行結果、戻す可能性のある素材

~/a10_cleanup_candidates/
  snapshot取得済みで、後日削除候補にできるもの
```

## 現時点の分類

### cleanup候補に近い

- `class_public_mess`
  - snapshot取得済み
  - 2GBの大半はgit pack二重など

### legacy_frozen推奨

- `class_hybrid_a10`
  - snapshot取得済み
  - ただしchain類やfinal runが重要な可能性あり
  - すぐ削除ではなくlegacy_frozenへ

### まだ診断が必要

- `class_unified_a10`
- `class_a10_2f`
- `class_old`
- `class_public`
- `a10_blackhole`

## すぐ消さないもの

- package.zip
- summary.json
- report.md
- manifest.json
- TeX/PDF
- final CSV
- final PNG
- MCMC chain full files
- CLASS modified source/header

## 消してもよい可能性が高いが、まだ一覧化後にするもの

- `__pycache__`
- `*.pyc`
- `.pytest_cache`
- venv
- build artifacts
- duplicated `.git` pack
- failed run bulk outputs

## 次の推奨ステップ

1. `class_unified_a10` のsnapshotを作る。
2. `class_public_mess` を `~/a10_cleanup_candidates/` へ移す。
3. root loose filesを `~/a10_legacy_frozen/root_loose_files_YYYYMMDD/` へ移す。
4. 削除は数日後、必要性がないと判断してから。


## v0.9追加: class_unified_a10

`class_unified_a10` のsnapshotを取得し、ハッブルテンションrepoへ統合した。

判定:

- 重要度: 最重要
- 元サイズ: 約12G
- snapshot: 約6.71 MB
- 推奨: 削除ではなく `~/a10_legacy_frozen/` へ移動

現時点のCLASS系整理:

```text
class_public_mess:
  snapshot取得済み
  cleanup_candidateへ移動可

class_hybrid_a10:
  snapshot取得済み
  legacy_frozen推奨

class_unified_a10:
  snapshot取得済み
  最重要。legacy_frozen推奨

class_a10_2f:
  まだ診断対象

class_old / class_public:
  比較元・clean source候補として保持
```


## v1.0追加: class_a10_2f

`class_a10_2f` のsnapshotを取得し、ハッブルテンションrepoへ統合した。

判定:

- 重要度: 中〜高
- 元サイズ: 約2.6G
- snapshot: 約7.52 MB
- 推奨: 削除ではなく `~/a10_legacy_frozen/` へ移動

現時点のCLASS系整理:

```text
class_public_mess:
  snapshot取得済み
  cleanup_candidateへ移動可

class_hybrid_a10:
  snapshot取得済み
  legacy_frozen推奨

class_unified_a10:
  snapshot取得済み
  最重要。legacy_frozen推奨

class_a10_2f:
  snapshot取得済み
  legacy_frozen推奨

class_old / class_public:
  比較元・clean source候補として保持

class_public_broken / class_public_broken_backup:
  snapshot不要ならcleanup_candidate候補
```


## v1.1追加: class_public_broken 系

`class_public_broken` と `class_public_broken_backup` のsnapshotを取得した。

判定:

- `class_public_broken`: cleanup_candidate
- `class_public_broken_backup`: cleanup_candidate

これにより、主要CLASS系のうち broken / backup 系は削除前保護が完了した。
