# A10 137-Gated Cosmology — Technical Visual Orientation v0.2.0

This add-on is a professional repository-facing visual orientation layer for the `a10-cosmology-137-gated` project.

It is intentionally **not** a fully beginner-oriented popular-science page. It assumes that the reader has at least some interest in cosmology, CMB constraints, numerical workflows, or reproducible preprints.

## Purpose

The page helps technically interested first-time readers understand:

- why the model uses both `z≈5000` localization and `χ≈137` gating,
- how the repository's evidence chain is organized,
- what should be inspected first,
- which parts carry stronger or weaker evidential weight,
- what the model does **not** claim.

## What it is not

It is not:

- a CLASS runner,
- a Cobaya runner,
- an MCMC dashboard,
- a substitute for the manuscript,
- a substitute for independent reproduction,
- a proof of the A10 branch,
- a popular-science simplification for general audiences.

## Installation

Copy this folder into the repository:

```text
a10-cosmology-137-gated/
  docs/
    technical_visual_orientation/
      index.html
      README_TECHNICAL_VISUAL_ORIENTATION.md
      TECHNICAL_VISUAL_ORIENTATION_SCOPE.md
```

Open in a browser:

```text
docs/technical_visual_orientation/index.html
```

No Python or internet connection is required.

## Recommended README snippet

```markdown
## Technical Visual Orientation

A browser-only technical visual orientation page is available at:

`docs/technical_visual_orientation/index.html`

This page is intended for technically interested first-time readers who want a structured overview of the model logic, repository evidence chain, and claim boundary before reading the manuscript and source/configuration materials. It does not run CLASS/Cobaya/MCMC and does not replace the numerical evidence.
```
