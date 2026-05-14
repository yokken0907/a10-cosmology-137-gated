import re

print("1. Repairing perturbations.h (Thread Safety)")
with open('include/perturbations.h', 'r') as f:
    text = f.read()

# グローバル共有領域(ppt)からA10の背番号を削除
text = re.sub(r'^\s*int\s+index_pt_delta_a10\s*;\n', '', text, flags=re.MULTILINE)
text = re.sub(r'^\s*int\s+index_pt_theta_a10\s*;\n', '', text, flags=re.MULTILINE)

# スレッド独立領域(ppv)の流体(fld)のすぐ下へA10の背番号を追加
if "int index_pt_delta_a10;" not in text:
    text = re.sub(r'(int\s+index_pt_delta_fld\s*;)', r'\1\n  int index_pt_delta_a10;\n  int index_pt_theta_a10;', text)

with open('include/perturbations.h', 'w') as f:
    f.write(text)

print("2. Repairing perturbations.c (Memory Access)")
with open('source/perturbations.c', 'r') as f:
    text = f.read()

# 全てのアクセスをスレッド独立の安全なポインタ(ppw->pv)に書き換え
text = text.replace("ppt->index_pt_delta_a10", "ppw->pv->index_pt_delta_a10")
text = text.replace("ppt->index_pt_theta_a10", "ppw->pv->index_pt_theta_a10")

# 新規作成時のみ自分自身(ppv)を指すように文脈補正
text = text.replace("ppw->pv->index_pt_delta_a10 = index_pt;", "ppv->index_pt_delta_a10 = index_pt;")
text = text.replace("ppw->pv->index_pt_theta_a10 = index_pt;", "ppv->index_pt_theta_a10 = index_pt;")
text = text.replace("ppv->y[ppw->pv->index_pt_delta_a10]", "ppv->y[ppv->index_pt_delta_a10]")
text = text.replace("ppv->y[ppw->pv->index_pt_theta_a10]", "ppv->y[ppv->index_pt_theta_a10]")

with open('source/perturbations.c', 'w') as f:
    f.write(text)

print("Fix completed.")
