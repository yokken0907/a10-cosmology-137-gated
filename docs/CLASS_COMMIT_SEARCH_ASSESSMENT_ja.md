# CLASS commit 検索で拾ったファイルの判定

## 結論

今回のアップロードだけでは、upstream CLASS の正確な commit hash は確定しない。

ただし、`CLASS_MANUAL.pdf` はローカルCLASSツリーの時期を推定する補助情報として有用である。一方、`pre-commit.sample` などの git hook sample は、Git が自動生成する汎用サンプルであり、A10 cosmology の再現性資料としては不要である。

## 採用判断

### 参考情報として採用

- `CLASS_MANUAL.pdf`

理由:
- Doxygen生成マニュアルであり、ローカルCLASS tree の documentation snapshot として扱える。
- ただし、公開GitHub本体に322ページPDFを同梱する必要はない。
- manifestにsha256とサイズだけ記録し、必要なら手元のlocal referenceとして保管する。

### 採用しない

- `pre-merge-commit.sample`
- `prepare-commit-msg.sample`
- `commit-msg.sample`
- `pre-commit.sample`

理由:
- これらは `.git/hooks/` に置かれる汎用sampleであり、commit hashや研究再現性を示すものではない。
- GitHub公開リポジトリには入れない。

## 分かったこと

- `CLASS_MANUAL.pdf` の表紙には `Last updated February 17, 2025` とある。
- これはA10改造に使われたCLASS treeが少なくともその時期以降のdocumentation snapshotを含んでいる可能性を示す。
- ただし、manualの更新日とsource commitは同一ではないため、これをupstream commitとして扱ってはいけない。

## 公開版での記載案

> The local CLASS documentation snapshot includes a Doxygen-generated CLASS manual last updated February 17, 2025. This is useful as contextual provenance, but it does not by itself identify the exact upstream CLASS commit used for the A10-modified source overlay.

日本語では:

> ローカルCLASS documentation snapshotには、2025年2月17日更新のDoxygen生成CLASS manualが含まれている。これは来歴推定の補助情報として有用だが、A10改造元の正確なupstream CLASS commitを同定するものではない。

## 現在の再現性ステータス

- local modified CLASS source/header overlay: あり
- zero-amplitude continuity repair diff: あり
- Cobaya YAML: あり
- MCMC summary: あり
- exact upstream CLASS commit: 未確定
- Planck/clikなど外部likelihood: GitHub同梱不可・local-only扱い

