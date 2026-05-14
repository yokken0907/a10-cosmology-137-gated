# class_public_broken / class_public_broken_backup snapshot assessment

## 結論

`class_public_broken` と `class_public_broken_backup` は、主要なA10 cosmology再現系ではなく、broken / backup 系のCLASS作業ツリーとして扱う。

今回、削除前保護用の小型snapshotを取得し、ハッブルテンションrepoへ統合した。

## class_public_broken

- 元サイズ: 約1.7G
- snapshot: 約3.21 MB / 202 files
- HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## class_public_broken_backup

- 元サイズ: 約879M
- snapshot: 約1.94 MB / 74 files
- HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 推奨扱い

- repo内snapshot: public repoに入れてよい小型来歴資料
- 元フォルダ: `~/a10_cleanup_candidates/` へ移動可
- 削除: すぐではなく、数日後に必要性がないことを確認してから

## 主要CLASS系の現状

```text
class_public_mess:
  snapshot取得済み
  cleanup_candidate

class_hybrid_a10:
  snapshot取得済み
  legacy_frozen

class_unified_a10:
  snapshot取得済み
  最重要 legacy_frozen

class_a10_2f:
  snapshot取得済み
  legacy_frozen

class_public_broken:
  snapshot取得済み
  cleanup_candidate

class_public_broken_backup:
  snapshot取得済み
  cleanup_candidate

class_public:
  clean/reference候補として保持

class_old:
  まだ診断または保持候補
```
