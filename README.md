# A10 Cosmology — 137-Gated Branch

This repository folder provides public-facing reproducibility materials for the A10 cosmology branch centered on localized early-time energy transfer and 137-stability gating.

It is intended to accompany the Jxiv preprint:

**From Localized Early-Time Energy Transfer to 137-Stability Gating: A Refined Integrated A10 Cosmology for the Hubble Tension with an Optional Late-Time Growth-Suppression Extension**

Jxiv DOI / URL: pending  
Public release status: prepared for post-Jxiv-publication GitHub staging

## What this repository contains

- manuscript references,
- claim-boundary statements,
- AI-assistance disclosure,
- local modified CLASS source/header overlay,
- zero-amplitude continuity repair notes/diffs,
- Cobaya YAML configuration materials,
- MCMC summary files,
- reproducibility status documents,
- data-requirement notes.

## What this repository does not contain

- Planck/clik likelihood data,
- full external likelihood packages,
- compiled CLASS binaries,
- `_classy` binary extensions,
- local `.git/` history,
- full final raw MCMC chain text files in the GitHub body. Compact legacy/provenance chain fragments and minimization summaries may be included where needed for auditability.

Large or non-redistributable assets are treated as local-only or future Zenodo/release-asset candidates.

## Scientific scope

The A10 137-gated branch is presented as a candidate high-H0 mechanism with numerical support in the reported workflow. It is **not** presented as:

- a definitive resolution of the Hubble tension,
- an established replacement for ΛCDM,
- a final observational model selection,
- a fully independent external reproduction,
- a claim that the number 137 is a universal cosmological constant.

## Reproducibility status

This archive provides a local modified CLASS/Cobaya reproducibility reference.

Important caveat:

> The exact upstream CLASS commit remains unreconstructed. The repository provides the local modified source overlay and configuration records used in the reported workflow, not a clean upstream patch release.

## Recommended citation

Use the Jxiv DOI once assigned. Until then, cite as:

Keiji Yoshimura, *From Localized Early-Time Energy Transfer to 137-Stability Gating: A Refined Integrated A10 Cosmology for the Hubble Tension with an Optional Late-Time Growth-Suppression Extension*, preprint, 2026.


## v0.7 update: class_public_mess legacy snapshot

A compact snapshot of the legacy WSL folder `class_public_mess` has been added under `legacy_class_worktrees/class_public_mess_snapshot/`.

This snapshot indicates that the legacy working tree was based on CLASS v3.3.4 / commit `e85808324f51fc694d12e3ed7439552a3c3f9540`. It is preserved as intermediate provenance material, not as a final clean upstream patch for the reported A10 unified run.


## v0.8 update: class_hybrid_a10 snapshot and root loose inventory

A compact snapshot of `class_hybrid_a10` has been added under `legacy_class_worktrees/class_hybrid_a10_snapshot_20260506_232834/`.

The snapshot indicates that this worktree was based on CLASS v3.3.4 / commit `e85808324f51fc694d12e3ed7439552a3c3f9540` and contains traces of A10 unified, SH0ES, run_B, run_C, and repaired_unified_highH0 workflows.

A local WSL root loose-file inventory has also been added under `local_wsl_inventory/root_loose_files_20260506_232931/`.


## v0.9 update: class_unified_a10 snapshot

A compact snapshot of `class_unified_a10` has been added under `legacy_class_worktrees/class_unified_a10_snapshot_20260506_234020/`.

This snapshot preserves key provenance for the unified A10 cosmology workflow, zero-continuity repair, high-H0 branch, and SH0ES/Planck/BAO/Pantheon-related materials. The original 12G worktree should not be committed to GitHub and should be moved to legacy frozen storage.


## v1.0 update: class_a10_2f snapshot

A compact snapshot of `class_a10_2f` has been added under `legacy_class_worktrees/class_a10_2f_snapshot_20260506_234458/`.

With this addition, compact preservation is complete for the main inspected A10 cosmology / CLASS legacy worktrees: `class_public_mess`, `class_hybrid_a10`, `class_unified_a10`, and `class_a10_2f`.


## v1.1 update: broken CLASS snapshots

Compact snapshots of `class_public_broken` and `class_public_broken_backup` have been added.  
They are treated as cleanup provenance, not as primary reproducibility sources.

## PUBLIC-GATE-0 status

Decision: `PASS-WITH-STRICT-COSMOLOGY-CLAIM-BOUNDARY-A10-COSMOLOGY-PUBLIC-GATE-0`  
Public version: `v0.1.1-public-gate`  
Classification: A10宇宙論137-gated branch再現性・来歴アーカイブ

This repository is a public-gate copy reviewed under an A10 Evidence-Lock Protocol style gate. The gate fixes the claim boundary, non-claims, manifest policy, and GitHub/Zenodo/Jxiv publication posture.

