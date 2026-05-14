import re

with open('a10_2f_ef.yaml', 'r') as f:
    text = f.read()

# 1. 念のため ln10^{10}A_s が残っていれば logA に置換
text = text.replace("ln10^{10}A_s", "logA")

# 2. CLASS に渡す際のパラメータ名をマッピング（Cobayaの正規の記法）
if "logA:" in text and "drop: true" in text:
    # 既存の余分なマッピング指定を削除
    text = re.sub(r"logA:\s*\n\s*value:\s*'lambda logA: logA'\n", "", text)
    
# 3. CLASS への橋渡し設定を theory: classy: の下に挿入
if "A_s" not in text:
    target = r"(extra_args:\n(?:.*?\n)*?)(?=\s*params:)"
    replacement = r"\1    renames:\n      A_s: 'lambda logA: 1e-10 * np.exp(logA)'\n"
    text = re.sub(target, replacement, text)

with open('a10_2f_ef.yaml', 'w') as f:
    f.write(text)
