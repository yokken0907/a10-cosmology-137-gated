# class_a10_2f_snapshot_20260506_234458

これは旧WSLフォルダ `~/class_a10_2f` から抽出した小型保護スナップショットである。

## 判定

- 元フォルダサイズ: 約2.6G
- snapshotサイズ: 約7.52 MB
- snapshot file count: 237
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 位置づけ

`class_a10_2f` は、A10 cosmology / CLASS系のlegacy branchとして保護する価値がある。  
名前から見て、two-field系または中間A10 branchの作業ツリーだった可能性がある。

## 公開上の扱い

このsnapshotはGitHub公開用repoに含められる小型来歴資料である。  
ただし、元の `class_a10_2f` 全体2.6Gを公開repoに入れてはいけない。

## 整理上の扱い

snapshot取得済みなので、元フォルダは `legacy_frozen` へ移動する候補。  
ただし、まだ固有のchain/outputが必要になる可能性があるため、即削除はしない。
