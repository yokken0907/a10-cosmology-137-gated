# class_unified_a10 snapshot assessment

## 結論

`class_unified_a10` は、現時点で確認したハッブルテンション/A10 cosmology系フォルダの中で最重要候補である。

今回のsnapshotにより、以下を確認した。

- 元フォルダサイズ: 約12G
- snapshot: 約6.71 MB / 163 files
- upstream/worktree HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- git log: `e8580832 (HEAD -> master, tag: v3.3.4, origin/master, origin/HEAD) Fixed shoorting bug (negative dx); store Omega_m(z) and Omega_r(z) in background table.`

## 意味

`class_unified_a10` は、名前・内容・keyword hitsから見て、A10 cosmology統合版の主要作業ツリーである可能性が高い。

以下の系統の痕跡が含まれる可能性が高い。

- unified A10
- repaired zero-continuity
- high-H0 branch
- SH0ES likelihood
- Planck / plik
- BAO
- Pantheon
- MCMC chain / covariance / checkpoint
- CLASS modified source/header
- build / external likelihood data

## 容量の主因

12G全体が必要コードという意味ではない。  
容量の主因は、おそらく以下の混在である。

1. `.git` pack
2. full MCMC chains
3. Planck/BAO/SN/Pantheon等の外部likelihood data
4. CLASS build artifacts
5. old/repaired/high-H0 output folders
6. virtual environment または package data

## 推奨扱い

- `class_unified_a10_snapshot_20260506_234020.tar.gz`: 保管推奨
- repo内snapshot: public GitHub repoに含めてもよい
- 元 `~/class_unified_a10`: 削除禁止。`legacy_frozen` へ移動推奨
- full chain files: 必要ならZenodo/release asset候補として別整理
- external likelihood data: GitHubに入れない

## cleanup判断

snapshot取得済みでも、`class_unified_a10` は最重要候補なので、まだ `cleanup_candidate` ではなく `legacy_frozen` 扱いが安全。
