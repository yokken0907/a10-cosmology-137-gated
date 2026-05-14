# GitHubに入れないもの

以下は公開リポジトリに入れない。

## 入れない

- `.git/`
- `class`
- `_classy.cpython-312-x86_64-linux-gnu.so`
- `build/`
- `*.o`
- `*.so`
- `*.a`
- Planck `.clik` likelihood data
- local-only Cobaya packages/data
- full MCMC chain txt files

## 理由

- `.git/` はローカル履歴であり、GitHub側で新しい履歴を作ればよい。
- `class` と `_classy...so` は環境依存のコンパイル済みバイナリであり、再現性資料としては不適切。
- 外部likelihood dataは第三者配布・サイズ・ライセンス上の問題がある。
- full chainは大容量なので、GitHub本体ではなくZenodoまたはrelease asset候補とする。

## 入れる

- source-level selected overlay
- YAML
- summary CSV/JSON
- patch notes
- manifest
- data requirements
- claim boundary
- AI assistance disclosure

