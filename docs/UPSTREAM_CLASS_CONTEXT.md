# Upstream CLASS context

This repository contains A10-related local overlay files for CLASS/Cobaya-style reproduction.

The uploaded CLASS README identifies the project as CLASS: Cosmic Linear Anisotropy Solving System, with download/clone instructions for `class_public`, and states the usual compilation workflow (`make clean; make class`) and publication citation requirements.

The uploaded `CLASS_rename.py` is a CLASS utility script whose header indicates that it can transform CLASS v2.10.8 into CLASS v3.0.0 and backwards. This is useful contextual evidence, but it is **not** by itself an exact upstream commit identifier for the A10 modified tree.

## Current status

- Local modified source/header overlay: available.
- Zero-amplitude continuity repair diff: available.
- Cobaya configuration and summary outputs: available.
- Exact upstream CLASS commit: still missing.

## Public release interpretation

Until the exact upstream commit is reconstructed, the public repository should describe the source files as a **local modified CLASS overlay** rather than as a clean, fully reproducible upstream patch.


## Additional context from uploaded CLASS manual

The uploaded `CLASS_MANUAL.pdf` is a Doxygen-generated CLASS manual with the visible timestamp “Last updated February 17, 2025.” This improves provenance context for the local tree, but does not replace an exact upstream git commit.

The uploaded `.sample` files from git hooks are not used.
