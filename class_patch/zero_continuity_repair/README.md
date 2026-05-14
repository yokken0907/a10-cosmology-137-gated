# Zero-amplitude continuity repair diffs

This directory contains diffs generated from the uploaded local backup folder:

- `patch_backup_zero_continuity_20260423_184427/*.bak` as the pre-repair local state
- `a10_repro_assets_collect/a10_class_and_chains_minimal/source/*.c` as the later repaired local state

These diffs are useful evidence for the **V0 -> 0 continuity repair** described in the technical follow-up manuscript. They are not guaranteed to be a clean upstream CLASS patch because the true upstream CLASS commit/version is still missing.

For public release, label this as a local repair diff, not as a complete installable patch.
