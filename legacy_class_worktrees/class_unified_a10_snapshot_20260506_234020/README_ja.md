# class_unified_a10_snapshot_20260506_234020

これは旧WSLフォルダ `~/class_unified_a10` から抽出した小型保護スナップショットである。

## 判定

- 元フォルダサイズ: 約12G
- snapshotサイズ: 約6.71 MB
- snapshot file count: 163
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 重要性

`class_unified_a10` は、これまで確認したCLASS系フォルダの中でも最重要候補である。  
名前・容量・keyword hitsから見て、A10 cosmology の統合版、zero-continuity repair、high-H0 branch、SH0ES/Planck/BAO/Pantheon関連workflowが含まれている可能性が高い。

## 公開上の扱い

このsnapshotはGitHub公開用repoに含められる小型来歴資料である。  
ただし、元の `class_unified_a10` 全体12Gを公開repoに入れてはいけない。

## 整理上の扱い

snapshot取得済みだが、元フォルダは最重要候補なので、削除ではなく `legacy_frozen` に移すことを推奨する。

full MCMC chain filesや外部likelihood dataを将来Zenodo等に置く可能性がある場合は、それらを別途archiveする。
