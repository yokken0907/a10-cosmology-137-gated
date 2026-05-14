# class_public_mess snapshot assessment

## 結論

`class_public_mess` は、削除前に小型保護スナップショットを取る価値のある legacy CLASS作業ツリーだった。

今回のsnapshotにより、少なくともこの作業ツリーについては次が確認できた。

- HEAD / commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`
- local diff: present
- snapshot size: 2.23 MB
- snapshot files: 72

## 意味

以前不足していた「upstream CLASS commit」の一部が埋まった。  
ただし、これは `class_public_mess` に限定される。

## まだ断言しないこと

- `class_unified_a10` の最終runが同一commit由来だったとはまだ断言しない。
- `class_hybrid_a10` の最終runが同一commit由来だったとはまだ断言しない。
- このsnapshot単体でハッブルテンション論文の最終再現性が完全に保証されるわけではない。

## 推奨扱い

- `class_public_mess` 本体2GB: snapshot取得後はcleanup候補
- `legacy_class_public_mess_snapshot.tar.gz`: 保管
- repo内snapshot: public repoに含めてもよい小型来歴資料
