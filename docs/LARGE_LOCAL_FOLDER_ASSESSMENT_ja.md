# 大型ローカルフォルダの採否判断

アップロードされた大型フォルダは、ハッブルテンション再現性アーカイブとして重要な素材を含んでいました。ただし、フォルダ丸ごとをGitHubへ貼り付けるのは不適切です。

## 採用したもの

- modified CLASS source/header overlay
- zero-amplitude continuity repair のローカルdiff
- 2026-04-23 source-level audit snapshot
- repaired unified high-H0 narrow rerun のYAML/config/progress/covmat/checkpoint
- local-only asset manifest / key file list

## 採用しないもの

- Planck 2018 likelihood data / `.clik` ディレクトリ
- BAO/SN likelihood data bundle
- compiled CLASS binaries / object files / build products
- full MCMC chain text files
- Cobaya packages全体

## 理由

GitHub公開用リポジトリは、第三者が構造を理解し、外部データを自分で取得して再現できるようにするための整理済みアーカイブであるべきです。ローカル実行環境全体をそのまま貼ると、サイズ・ライセンス・不要ファイル混入・再現手順の不透明化の問題が出ます。
