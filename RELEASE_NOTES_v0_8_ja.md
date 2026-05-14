# Release notes v0.8

## 追加内容

- `legacy_class_worktrees/class_hybrid_a10_snapshot_20260506_232834/`
- `legacy_class_worktrees/class_hybrid_a10_snapshot_assessment.json`
- `docs/CLASS_HYBRID_A10_SNAPSHOT_ASSESSMENT_ja.md`
- `local_wsl_inventory/root_loose_files_20260506_232931/`
- `local_wsl_inventory/root_loose_files_assessment.json`
- `docs/ROOT_LOOSE_FILES_ASSESSMENT_ja.md`
- `docs/WSL_CLEANUP_STRATEGY_ja.md`

## 確認事項

`class_hybrid_a10` は CLASS v3.3.4 / commit `e85808324f51fc694d12e3ed7439552a3c3f9540` を基点にした重要なA10 cosmology legacy worktreeである。

## 整理判断

- `class_public_mess`: snapshot取得済み。cleanup候補。
- `class_hybrid_a10`: snapshot取得済み。ただし重要度が高いため、削除ではなくlegacy_frozen推奨。
- root loose Python files: 容量は小さいが心理的散らかりの原因。削除ではなくlegacy_frozenへ移動推奨。
