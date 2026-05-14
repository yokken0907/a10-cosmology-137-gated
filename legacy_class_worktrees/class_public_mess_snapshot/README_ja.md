# class_public_mess_snapshot

これは、旧WSLフォルダ `~/class_public_mess` から抽出した小型保護スナップショットである。

## 判定

- 元フォルダ全体は約2GBだったが、その大半は `.git` packの二重保持やbuild/output類と推定される。
- このsnapshotは約2.23 MB、72 filesであり、公開・保管しやすい。
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`
- local diff: `class_public_mess_local_diff.patch`

## 位置づけ

このsnapshotは、A10/dNeff/S8探索に使われた可能性のある legacy CLASS作業ツリーの来歴・差分・設定・小型スクリプト保護用である。

## 注意

これは最終ハッブルテンションMCMC本命runを完全に証明するものではない。  
`class_unified_a10` や `class_hybrid_a10` など、他のCLASS作業ツリーの来歴は別途確認が必要である。

## 公開上の扱い

GitHub公開時には、以下のように説明する。

> A legacy working tree snapshot named `class_public_mess` was based on CLASS v3.3.4 / commit `e85808324f51fc694d12e3ed7439552a3c3f9540` and is preserved here only as an intermediate provenance record. It is not claimed as the final clean upstream patch for the reported A10 cosmology run.
