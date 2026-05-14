#!/usr/bin/env python3
import subprocess, re
from pathlib import Path

cases = [
    "bridge_eval_C_runB_fixed137_control_v3.yaml",
    "bridge_AC_interp_t0p0.yaml",
    "bridge_AC_interp_t0p25.yaml",
    "bridge_AC_interp_t0p5.yaml",
    "bridge_AC_interp_t0p75.yaml",
    "bridge_AC_interp_t1p0.yaml",
]
outdir = Path("chains")
summary = outdir / "bridge_C_and_AC_summary.tsv"
summary.write_text("case\tstatus\tloglike\tchi2_CMB\tchi2_SN\tchi2_shoes\terror_hint\n", encoding="utf-8")

patterns = {
    "loglike": re.compile(r"\[evaluate\] log-likelihood = ([^\n]+)"),
    "chi2_CMB": re.compile(r"\[evaluate\]\s+chi2__CMB = ([^\n]+)"),
    "chi2_SN": re.compile(r"\[evaluate\]\s+chi2__SN = ([^\n]+)"),
    "chi2_shoes": re.compile(r"\[evaluate\]\s+chi2_shoes_H0 = ([^\n]+)"),
}
errpat = re.compile(r"(Step size too small:[^\n]+|classy\._classy\.[A-Za-z]+Error:|Error in Class:[^\n]+)")

for case in cases:
    log = outdir / (Path(case).stem + ".stdout.log")
    proc = subprocess.run(["cobaya-run", case, "--force"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log.write_text(proc.stdout, encoding="utf-8")
    status = "ok" if proc.returncode == 0 else "fail"
    vals = {k:"nan" for k in patterns}
    if status == "ok":
        for k,p in patterns.items():
            m = p.search(proc.stdout)
            if m: vals[k] = m.group(1).strip()
    err = ""
    m = errpat.search(proc.stdout)
    if m:
        err = m.group(1).strip()
    with summary.open("a", encoding="utf-8") as f:
        f.write(f"{Path(case).stem}\t{status}\t{vals['loglike']}\t{vals['chi2_CMB']}\t{vals['chi2_SN']}\t{vals['chi2_shoes']}\t{err}\n")

print(f"Wrote {summary}")
print(summary.read_text(encoding='utf-8'))
