#!/usr/bin/env python3
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "class_hybrid_a10"
prefix = sys.argv[2] if len(sys.argv) > 2 else "repaired_unified_highH0_narrow"
chains_dir = ROOT / "chains"

files = sorted(chains_dir.glob(f"{prefix}.[0-9]*.txt"))
if not files:
    raise SystemExit(f"No chain files found for prefix {prefix!r} in {chains_dir}")

dfs = []
for f in files:
    df = pd.read_csv(f, delim_whitespace=True, comment="#")
    df["__source_file__"] = f.name
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

required = ["weight", "minuslogpost"]
for c in required:
    if c not in df.columns:
        raise SystemExit(f"Required column missing: {c}")

summary_cols = [
    "H0", "omega_b", "omega_cdm", "A_s", "n_s", "tau_reio",
    "log10_ua10_V0", "chi2__BAO", "chi2__CMB", "chi2__SN", "chi2__shoes_H0"
]
summary_cols = [c for c in summary_cols if c in df.columns]

w = df["weight"].to_numpy(dtype=float)
w = np.where(np.isfinite(w) & (w > 0), w, 0.0)
if w.sum() <= 0:
    raise SystemExit("Non-positive total weight")

def weighted_quantile(x, w, qs):
    order = np.argsort(x)
    x = x[order]
    w = w[order]
    cdf = np.cumsum(w)
    cdf = cdf / cdf[-1]
    return np.interp(qs, cdf, x)

rows = []
for col in summary_cols:
    x = df[col].to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(w) & (w > 0)
    if not mask.any():
        continue
    xm = x[mask]
    wm = w[mask]
    mean = np.average(xm, weights=wm)
    var = np.average((xm - mean) ** 2, weights=wm)
    q16, q50, q84 = weighted_quantile(xm, wm, [0.16, 0.50, 0.84])
    rows.append({
        "parameter": col,
        "weighted_mean": mean,
        "weighted_std": np.sqrt(var),
        "q16": q16,
        "q50": q50,
        "q84": q84,
        "minus_q16": q50 - q16,
        "plus_q84": q84 - q50,
    })

summary = pd.DataFrame(rows)

best_idx = df["minuslogpost"].astype(float).idxmin()
best = df.loc[[best_idx]].copy()

out_summary = chains_dir / f"{prefix}.summary.tsv"
out_best = chains_dir / f"{prefix}.bestpoint.tsv"
summary.to_csv(out_summary, sep="\t", index=False)
best.to_csv(out_best, sep="\t", index=False)

print(f"Wrote {out_summary}")
print(f"Wrote {out_best}")
print()
print(summary.to_string(index=False))
print()
print("Best point:")
print(best.to_string(index=False))
