# class_hybrid_a10 snapshot assessment

## 結論

`class_hybrid_a10` は、ハッブルテンション/A10 cosmology 系ではかなり重要なlegacy worktreeである。

今回のsnapshotにより、以下を確認した。

- 元フォルダサイズ: 約4.8G
- snapshot: 約12.84 MB / 1241 files
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> main, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 容量の主因

`top_500_files.tsv` から、容量の主因はおおむね以下である。

1. `.git/objects/pack`  
2. MCMC chain text files  
3. Planck/BAO/SN likelihood/data packages  
4. build / venv artifacts  
5. repaired_unified や run_B/run_C 系の中間保存

つまり、4.8G全体が必要コードというわけではない。

## 重要な中身

以下の名前が確認されているため、A10 cosmology公開repoでは保護価値がある。

- `unified_a10.yaml`
- `a10_phase4_shoes.yaml`
- `run_B_fixed137`
- `run_C_freegate`
- `repaired_unified_highH0_narrow`
- `patch_backup_zero_continuity_20260423_184427`
- `ua10_` 関連パラメータ
- SH0ES / Pantheon / BAO / Planck 関連設定

## 推奨扱い

- `class_hybrid_a10_snapshot_20260506_232834.tar.gz`: 保管推奨
- repo内snapshot: public repoへ入れてよい
- 元 `~/class_hybrid_a10`: すぐ削除ではなく `legacy_frozen` または `cleanup_candidate` へ移動候補
- full chain files: Zenodo等で公開する可能性があるなら、別途full-chain archiveとして扱う

## まだ注意すること

このsnapshotは公開repo統合用として十分小さいが、full chain filesや外部likelihood dataは含まない。  
したがって、完全なMCMC再現アーカイブではなく、legacy provenance snapshotとして扱う。
