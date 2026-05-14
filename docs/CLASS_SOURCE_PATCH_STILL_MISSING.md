# CLASS source patch still missing

The recovered `legacy_config_diffs/` files are useful Cobaya/YAML configuration diffs, but they do **not** provide the source-level CLASS implementation patch.

Still needed for a stronger public reproducibility repository:

1. Upstream CLASS version or commit used for the A10 modification.
2. Source-level diff for modified files, ideally:
   - `source/background.c`
   - `source/input.c`
   - `source/perturbations.c`
   - `include/background.h`
   - `include/input.h`
   - `include/perturbations.h`
3. Build instructions for the modified CLASS tree.
4. Cobaya environment and likelihood placement instructions.
5. Mapping from YAML/config files to paper tables and figures.

Until these are supplied, the public repository should be described as an AI-assisted reproducibility archive with partial configuration/material support, not as a complete one-command reproduction package.


## Update from uploaded local folder (v0.3)

The uploaded large local folder supplied useful source-level material:

- current modified CLASS source/header overlay
- source-level audit snapshot from 2026-04-23
- local pre/post zero-amplitude continuity repair diffs for three `.c` files
- repaired-unified Cobaya YAML files

Still missing for a truly clean public reproduction:

- exact upstream CLASS version / commit
- an upstream-to-A10 `git diff` generated from that clean base
- verified build instructions from a fresh checkout
- local likelihood installation instructions independent of private paths
