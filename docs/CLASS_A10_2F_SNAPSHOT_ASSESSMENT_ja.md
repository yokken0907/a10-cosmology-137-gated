# class_a10_2f snapshot assessment

## 結論

`class_a10_2f` は、A10 cosmology / CLASS系のlegacy branchとして小型snapshot化できた。

今回のsnapshotにより、以下を確認した。

- 元フォルダサイズ: 約2.6G
- snapshot: 約7.52 MB / 237 files
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 意味

`class_a10_2f` は、`class_unified_a10` ほど最重要とは限らないが、A10 cosmologyの中間branchまたはtwo-field branchとして保護価値がある。

## 推奨扱い

- `class_a10_2f_snapshot_20260506_234458.tar.gz`: 保管推奨
- repo内snapshot: public GitHub repoに含めてもよい
- 元 `~/class_a10_2f`: 削除ではなく `legacy_frozen` へ移動推奨

## 注意

このsnapshotだけで最終ハッブルテンション結果を代表させない。  
最終候補は `class_unified_a10` と `class_hybrid_a10` のsnapshotを優先する。
