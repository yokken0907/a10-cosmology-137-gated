import re

with open('source/input.c', 'r') as f:
    text = f.read()

# 1. A10パラメータの読み込みブロックを抽出
match = re.search(r'(/\*\s*=====\s*A10-2F-EF Background Parameters\s*=====\s*\*/.*?/\*\s*===========================================\s*\*/)', text, re.DOTALL)

if match:
    a10_block = match.group(1)
    
    # 2. 元の場所（fldブロックの中）からA10ブロックを削除
    text = text.replace(a10_block, "/* A10 block moved to global scope */\n")
    
    # 3. fldブロックの終了カッコ } の直後に、A10ブロックを「独立して」挿入
    # 通常、fldブロックの終わりは scfブロックの始まりの直前です
    target_pos = r"(/\*\*\s*8\.b\)\s*If Omega scalar field \(SCF\))"
    replacement = a10_block + r"\n\n\n  \1"
    
    text = re.sub(target_pos, replacement, text)
    
    with open('source/input.c', 'w') as f:
        f.write(text)
    print("SUCCESS: A10 parser successfully decoupled from fluid parameters.")
else:
    print("WARNING: Could not find A10 block. It might already be moved.")

