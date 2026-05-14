#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

yaml_names = [
    "bridge_A_homotopy_V0_5000.yaml",
    "bridge_A_homotopy_V0_1000.yaml",
    "bridge_A_homotopy_V0_100.yaml",
    "bridge_A_homotopy_V0_10.yaml",
    "bridge_A_homotopy_V0_1.yaml",
    "bridge_A_homotopy_V0_1em02.yaml",
    "bridge_A_homotopy_V0_1em04.yaml",
    "bridge_A_homotopy_V0_0.yaml",
]

chains = Path("chains")
chains.mkdir(exist_ok=True)
summary = chains / "bridge_A_homotopy_summary.tsv"
summary.write_text("prefix\tua10_V0\tstatus\tloglike\tchi2_CMB\tchi2_SN\tchi2_shoes\terror_hint\n", encoding="utf-8")

patterns = {
    "loglike": re.compile(r"\[evaluate\] log-likelihood = ([^\n]+)"),
    "chi2_CMB": re.compile(r"\[evaluate\]\s+chi2__CMB = ([^\n]+)"),
    "chi2_SN": re.compile(r"\[evaluate\]\s+chi2__SN = ([^\n]+)"),
    "chi2_shoes": re.compile(r"\[evaluate\]\s+chi2_shoes_H0 = ([^\n]+)"),
}
error_patterns = [
    re.compile(r"Step size too small:[^\n]+"),
    re.compile(r"Class did not read input parameter\(s\):[^\n]+"),
    re.compile(r"Failed to load external function:[^\n]+"),
]

def extract(pat, text):
    m = pat.search(text)
    return m.group(1).strip() if m else "nan"

for yaml_name in yaml_names:
    prefix = yaml_name.replace(".yaml","")
    stdout_log = chains / f"{prefix}.stdout.log"
    proc = subprocess.run(["cobaya-run", yaml_name, "--force"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    stdout_log.write_text(proc.stdout, encoding="utf-8")
    status = "ok" if proc.returncode == 0 else "fail"
    values = {k: extract(p, proc.stdout) for k,p in patterns.items()}
    error_hint = ""
    for ep in error_patterns:
        m = ep.search(proc.stdout)
        if m:
            error_hint = m.group(0)
            break
    v0_token = prefix.split("_V0_")[-1]
    summary.open("a", encoding="utf-8").write(
        f"{prefix}\t{v0_token}\t{status}\t{values['loglike']}\t{values['chi2_CMB']}\t{values['chi2_SN']}\t{values['chi2_shoes']}\t{error_hint}\n"
    )
    print(f"=== {prefix}: {status} ===")

print(f"\nWrote {summary}")
