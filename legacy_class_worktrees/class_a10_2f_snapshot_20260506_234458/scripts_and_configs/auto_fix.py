import re

# 1. perturbations.h の確実な修正
try:
    with open('include/perturbations.h', 'r') as f:
        content = f.read()
    # 重複・散乱した変数を削除
    content = re.sub(r'^\s*short has_perturbations_a10;.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*int a10_cs_model;.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*int index_pt_delta_a10;.*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*int index_pt_theta_a10;.*?\n', '', content, flags=re.MULTILINE)
    
    # 構造体の先頭（struct perturbations { の直後）に確実に追加
    target = r"(struct\s+perturbations\s*\{)"
    replacement = r"\1\n  short has_perturbations_a10;\n  int a10_cs_model;\n  int index_pt_delta_a10;\n  int index_pt_theta_a10;\n"
    content = re.sub(target, replacement, content, count=1)
    
    with open('include/perturbations.h', 'w') as f:
        f.write(content)
except Exception as e:
    print("Header fix error:", e)

# 2. perturbations.c のスコープ修正
try:
    with open('source/perturbations.c', 'r') as f:
        content = f.read()
    
    # perturbations_total_stress_energy 内の pvecback アクセスエラーを修正
    content = content.replace("ppw->pvecback[pba->index_bg_rho_a10]", "pvecback[pba->index_bg_rho_a10]")
    content = content.replace("pvecback[pba->index_bg_rho_a10]", "ppw->pvecback[pba->index_bg_rho_a10]")
    
    content = content.replace("ppw->pvecback[pba->index_bg_p_a10]", "pvecback[pba->index_bg_p_a10]")
    content = content.replace("pvecback[pba->index_bg_p_a10]", "ppw->pvecback[pba->index_bg_p_a10]")

    # 変数ポインタの取り違え(ppv -> ppt)を修正
    content = content.replace("ppv->index_pt_delta_a10", "ppt->index_pt_delta_a10")
    content = content.replace("ppv->index_pt_theta_a10", "ppt->index_pt_theta_a10")
    
    with open('source/perturbations.c', 'w') as f:
        f.write(content)
except Exception as e:
    print("Source fix error:", e)

