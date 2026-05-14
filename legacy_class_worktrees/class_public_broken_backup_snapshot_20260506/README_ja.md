# class_public_broken_backup_snapshot_20260506

これは旧WSLフォルダ `~/class_public_broken_backup` から抽出した小型保護スナップショットである。

## 判定

- 元フォルダサイズ: 879M
- snapshotサイズ: 約1.94 MB
- snapshot file count: 74
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 位置づけ

`class_public_broken_backup` は、名前通り broken / backup 系のCLASS作業ツリーであり、ハッブルテンション再現の主系統ではない。
ただし、削除前の来歴保護としてsnapshotを保存する価値がある。

## 整理上の扱い

snapshot取得済みなので、元フォルダは `cleanup_candidates` へ移動してよい候補である。
ただし、削除は数日置いてから、必要なものがないことを確認して行う。
