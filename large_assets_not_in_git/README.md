# Large/local assets deliberately not included in Git

The uploaded local folder contained large and/or third-party assets. They are intentionally not copied into this GitHub-ready folder.

Do not commit directly to GitHub:

- Planck 2018 likelihood data / `.clik` directories
- BAO/SN likelihood data bundles copied from local Cobaya packages
- compiled CLASS binaries, object files, build directories, `libclass.a`, `.so` files
- full MCMC chain text files of tens of MB each

Use this repository to document how those assets are obtained or where they should be placed locally. Full chain files, if published, should be placed in a GitHub Release asset or Zenodo archive, not the main repository tree.
