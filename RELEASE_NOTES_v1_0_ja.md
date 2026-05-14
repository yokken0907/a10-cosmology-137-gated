# Release notes v1.0

## 追加内容

- `legacy_class_worktrees/class_a10_2f_snapshot_20260506_234458/`
- `legacy_class_worktrees/class_a10_2f_snapshot_assessment.json`
- `docs/CLASS_A10_2F_SNAPSHOT_ASSESSMENT_ja.md`
- `docs/WSL_CLEANUP_STRATEGY_ja.md` 追記

## 確認事項

`class_a10_2f` はA10 cosmology / CLASS系のlegacy branchとして保護価値がある。

## 整理判断

主要なA10 cosmology / CLASS legacy worktreeの小型保護は一区切り。

- `class_public_mess`: snapshot取得済み。cleanup候補。
- `class_hybrid_a10`: snapshot取得済み。legacy_frozen推奨。
- `class_unified_a10`: snapshot取得済み。最重要。legacy_frozen推奨。
- `class_a10_2f`: snapshot取得済み。legacy_frozen推奨。

次に容量を減らすなら、削除ではなく移動で整理する。
