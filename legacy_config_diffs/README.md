# Legacy Cobaya config diffs

This folder contains two small historical configuration diffs recovered from an ad-hoc local search.
They are useful as provenance material for the A10 cosmology workflow, but they are **not** the missing CLASS source-code patch.

Included:

- `legacy_eval_hasA10_vs_bridgeA_config.diff`  
  Compares a sampled/prior-style `run_C_eval_has_a10.yaml` setup against a fixed best-point/evaluate-style `bridge_eval_A_scan730_best_v2.yaml` setup.

- `legacy_bridgeA_vs_bridgeC_config.diff`  
  Compares `bridge_eval_A_scan730_best_v2.yaml` with a later `bridge_eval_C_runB_fixed137_control_v3.yaml` fixed-trigger control/evaluate setup.

Use these only as historical reproducibility/provenance notes. They should not be advertised as a complete rerun recipe.
