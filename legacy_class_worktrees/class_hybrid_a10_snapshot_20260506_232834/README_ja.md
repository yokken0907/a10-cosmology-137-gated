# class_hybrid_a10_snapshot_20260506_232834

これは旧WSLフォルダ `~/class_hybrid_a10` から抽出した小型保護スナップショットである。

## 判定

- 元フォルダサイズ: 約4.8G
- snapshotサイズ: 約12.84 MB
- snapshot file count: 1241
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> main, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 重要性

`class_hybrid_a10` は、ハッブルテンション/A10 cosmology でかなり重要な作業ツリーである可能性が高い。

痕跡として、以下が確認されている。

- `unified_a10.yaml`
- `a10_phase4_shoes.yaml`
- `run_B_fixed137`
- `run_C_freegate`
- `repaired_unified_highH0_narrow`
- SH0ES / Pantheon / BAO / Planck 関連の設定・出力
- chain outputs
- packages/data 内の外部likelihood/data
- `.venv_a10build`
- build artifacts

## 公開上の扱い

このsnapshotはGitHub公開用repoに含められる小型来歴資料である。  
ただし、元の `class_hybrid_a10` 全体を公開repoに入れてはいけない。

## 整理上の扱い

snapshot取得済みなので、元の巨大フォルダは「削除」ではなく、まず `cleanup_candidate` または `legacy_frozen` に移す候補となる。

ただし、full chain filesを将来Zenodoに置く可能性がある場合は、chain類だけ別途保護してから整理する。
