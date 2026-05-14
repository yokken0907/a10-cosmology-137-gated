# アップロードされたCLASS関連素材の判定

## 結論

`.git` フォルダは不要です。GitHub公開用のリポジトリに、ローカルの `.git` 履歴を丸ごと貼る必要はありません。

今回アップロードされた素材の扱いは次の通りです。

## 採用する素材

- `source.zip`
- `include.zip`
- `README(202).md`
- `CLASS_rename.py`

ただし、`source.zip` と `include.zip` の全ファイルを公開版にそのまま入れるのではなく、A10改造に直接関係する selected overlay と manifest として扱う。

## 採用しない素材

- `class`
- `_classy.cpython-312-x86_64-linux-gnu.so`

これらはコンパイル済みバイナリであり、公開GitHubには入れない。

## 今回分かったこと

- selected modified overlay として必要な `background.c`, `input.c`, `perturbations.c`, `background.h`, `input.h`, `perturbations.h` は既に v0.3 の `class_patch/current_source_overlay/` に入っている。
- 今回の `source.zip` / `include.zip` は、その selected overlay と整合するローカルCLASS snapshotとして扱える。
- ただし、upstream CLASS の正確な commit hash はまだ未確定。

## まだ足りないもの

最も望ましい追加情報は、元にした upstream CLASS の正確な version / commit である。

もし見つからなければ、公開版では以下のように書く。

> This archive provides the local modified source overlay and configuration files used in the reported run. The exact upstream CLASS commit remains to be reconstructed; users should treat the overlay as a local reproducibility reference rather than a clean upstream patch.

