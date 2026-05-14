# Release notes v1.1

## 追加内容

- `legacy_class_worktrees/class_public_broken_snapshot_20260506/`
- `legacy_class_worktrees/class_public_broken_backup_snapshot_20260506/`
- `legacy_class_worktrees/class_public_broken_snapshot_assessment.json`
- `legacy_class_worktrees/class_public_broken_backup_snapshot_assessment.json`
- `docs/CLASS_BROKEN_SNAPSHOTS_ASSESSMENT_ja.md`
- `docs/WSL_CLEANUP_STRATEGY_ja.md` 追記

## 整理判断

`class_public_broken` と `class_public_broken_backup` は、snapshot取得済みのため `cleanup_candidates` へ移動してよい。

削除は即時ではなく、数日後に必要性がないことを確認してから。
