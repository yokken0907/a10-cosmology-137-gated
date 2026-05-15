# README regeneration instructions

Replace the repository root files with these regenerated files:

```text
README.md
README_ja.md
```

Recommended Git commands:

```bash
cd ~/path/to/a10-cosmology-137-gated
cp /path/to/README.md README.md
cp /path/to/README_ja.md README_ja.md

git diff -- README.md README_ja.md
git add README.md README_ja.md
git commit -m "Update README with technical visual orientation"
git push
```

If the technical visual orientation folder is not yet added, add it in the same commit:

```bash
git add docs/technical_visual_orientation README.md README_ja.md
git commit -m "Add technical visual orientation and update README"
git push
```

This is a documentation update. No new Zenodo DOI is required.
