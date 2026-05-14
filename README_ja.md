# A10 Cosmology — 137-Gated Branch

このフォルダは、A10宇宙論のうち、局所的early-time energy transferと137-stability gatingを中心とするハッブルテンション候補機構の公開用再現資料である。

対応するJxiv論文:

**From Localized Early-Time Energy Transfer to 137-Stability Gating: A Refined Integrated A10 Cosmology for the Hubble Tension with an Optional Late-Time Growth-Suppression Extension**

Jxiv DOI / URL: pending  
公開状態: Jxiv掲載後のGitHub staging用

## 含まれるもの

- 論文参照資料
- 主張境界
- AI支援開示
- A10改造後のローカルCLASS source/header overlay
- zero-amplitude continuity repair notes/diffs
- Cobaya YAML
- MCMC summary
- 再現性ステータス文書
- 外部データ要件メモ

## 含まれないもの

- Planck/clik likelihood data
- 外部likelihood package全体
- compiled CLASS binaries
- `_classy` binary extension
- `.git/` 履歴
- 最終版のfull raw MCMC chain text files（ただし監査用の小型legacy/provenance chain断片やminimization summaryは含まれる場合がある）

大容量または再配布に注意が必要なものは、local-onlyまたは将来のZenodo/release asset候補として扱う。

## 科学的スコープ

A10 137-gated branchは、報告されたworkflowにおいて数値的支持を受けた高H0候補機構として提示する。以下は主張しない。

- ハッブルテンションの決定的解決
- ΛCDMの確立済み置換
- 観測的な最終モデル選択
- 完全な外部独立再現
- 数値137が普遍的宇宙定数であること

## 再現性ステータス

本アーカイブは、A10改造後のローカルCLASS/Cobaya再現性資料である。

重要な注意:

> 元にしたupstream CLASSの正確なcommitは未確定である。本リポジトリは、報告workflowで使用されたローカルmodified source overlayと設定記録を提供するものであり、clean upstream patch releaseではない。

## 引用

Jxiv DOIが付与されたら、そのDOIを優先して引用する。現時点では以下。

Keiji Yoshimura, *From Localized Early-Time Energy Transfer to 137-Stability Gating: A Refined Integrated A10 Cosmology for the Hubble Tension with an Optional Late-Time Growth-Suppression Extension*, preprint, 2026.


## v0.7 update: class_public_mess legacy snapshot

旧WSLフォルダ `class_public_mess` の小型スナップショットを `legacy_class_worktrees/class_public_mess_snapshot/` に追加した。

このsnapshotにより、少なくとも当該作業ツリーは CLASS v3.3.4 / commit `e85808324f51fc694d12e3ed7439552a3c3f9540` を基点にしていたことが確認できる。ただし、これは最終A10 unified runの完全なupstream証明ではなく、中間探索・来歴保護資料として扱う。


## v0.8 update: class_hybrid_a10 snapshot and root loose inventory

`class_hybrid_a10` の小型snapshotを `legacy_class_worktrees/class_hybrid_a10_snapshot_20260506_232834/` に追加した。

このsnapshotにより、当該worktreeが CLASS v3.3.4 / commit `e85808324f51fc694d12e3ed7439552a3c3f9540` を基点としていること、A10 unified / SH0ES / run_B / run_C / repaired_unified_highH0 系の痕跡を含むことが確認できた。

また、WSLホーム直下のloose Python filesのinventoryを `local_wsl_inventory/root_loose_files_20260506_232931/` に追加した。


## v0.9 update: class_unified_a10 snapshot

`class_unified_a10` の小型snapshotを `legacy_class_worktrees/class_unified_a10_snapshot_20260506_234020/` に追加した。

このsnapshotにより、A10 cosmology統合版・zero-continuity repair・high-H0 branch・SH0ES/Planck/BAO/Pantheon関連workflowの主要来歴を保護した。元フォルダ全体12GはGitHubに入れず、legacy_frozenへ移動することを推奨する。


## v1.0 update: class_a10_2f snapshot

`class_a10_2f` の小型snapshotを `legacy_class_worktrees/class_a10_2f_snapshot_20260506_234458/` に追加した。

これにより、主要なA10 cosmology / CLASS legacy worktreeのうち、`class_public_mess`, `class_hybrid_a10`, `class_unified_a10`, `class_a10_2f` の小型保護が完了した。


## v1.1 update: broken CLASS snapshots

`class_public_broken` と `class_public_broken_backup` の小型snapshotを追加した。  
これらは主要再現系ではなく、cleanup前の来歴保護資料として扱う。

## PUBLIC-GATE-0 status

判定: `PASS-WITH-STRICT-COSMOLOGY-CLAIM-BOUNDARY-A10-COSMOLOGY-PUBLIC-GATE-0`  
公開版: `v0.1.1-public-gate`  
分類: A10宇宙論137-gated branch再現性・来歴アーカイブ

このリポジトリは、A10 Evidence-Lock Protocol型の公開前監査により、主張境界・非主張事項・manifest整合性・GitHub/Zenodo/Jxiv方針を固定した public-gate 版である。

