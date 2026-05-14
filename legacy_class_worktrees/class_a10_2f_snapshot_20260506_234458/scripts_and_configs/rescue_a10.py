import re

with open('source/perturbations.c', 'r') as f:
    content = f.read()

# 1. ゲージ依存の未定義ポインタ参照を修正（Segfaultの主原因1）
content = content.replace("0.5 * ppw->pvecmetric[ppw->index_mt_h_prime]", "metric_continuity")

# 2. 速度方程式における metric_euler の欠落を修正
if "metric_euler - a_a10" not in content:
    content = content.replace("- a_a10 * Gamma_a10 * y[ppt->index_pt_theta_a10];", "+ metric_euler - a_a10 * Gamma_a10 * y[ppt->index_pt_theta_a10];")

# 3. 配列外参照（バッファオーバーフロー）を防止（Segfaultの主原因2）
content = re.sub(r'if\s*\(\s*ppt->has_perturbations_a10\s*==\s*_TRUE_\s*\)\s*\{\s*ppt->index_pt_delta_a10\s*=\s*index_pt;\s*index_pt\+\+;\s*ppt->index_pt_theta_a10\s*=\s*index_pt;\s*index_pt\+\+;\s*\}', '', content)

# メモリ確保（pt_size = index_pt;）の直前に強制挿入し、配列サイズを確定させる
if "A10-2F-EF indices (Safe Allocation)" not in content:
    target = r"(ppv->pt_size\s*=\s*index_pt;)"
    replacement = r"/* A10-2F-EF indices (Safe Allocation) */\n  if (ppt->has_perturbations_a10 == _TRUE_) {\n    ppt->index_pt_delta_a10 = index_pt;\n    index_pt++;\n    ppt->index_pt_theta_a10 = index_pt;\n    index_pt++;\n  }\n  \1"
    content = re.sub(target, replacement, content, count=1)

with open('source/perturbations.c', 'w') as f:
    f.write(content)
