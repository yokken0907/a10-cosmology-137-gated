# Current CLASS source overlay (local reproduction asset)

This directory contains the six modified CLASS source/header files recovered from the local reproduction folder.

These files are **not** an upstream-clean patch by themselves. They are included as a local source overlay for reproducibility triage. For a public repository, prefer an upstream-based `git diff` if the original CLASS commit/version can be identified.

Included files:

- `source/background.c`
- `source/input.c`
- `source/perturbations.c`
- `include/background.h`
- `include/input.h`
- `include/perturbations.h`

Claim boundary: this overlay supports reproducibility of the reported A10 runs; it does not establish final cosmological model selection.
