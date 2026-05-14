import subprocess

# 探索範囲
f_list = [0.130, 0.132, 0.134, 0.136, 0.138, 0.140]
z_star = 3000.0

print(f"{'f_star':>10} | {'rs':>12} | {'100*theta_s':>12}")
print("-" * 45)

for f in f_list:
    # 1. 宇宙を成立させるために必要な最小限のパラメータをすべて書き込む
    with open("my_theory.ini", "w") as f_ini:
        f_ini.write(f"H0 = 72.6397\n")
        f_ini.write(f"Omega_b = 0.0486\n") # 標準的なバリオン量
        f_ini.write(f"Omega_cdm = 0.2589\n") # 標準的なダークマター量
        f_ini.write(f"z_star_yoshimura = {z_star}\n")
        f_ini.write(f"f_star_yoshimura = {f}\n")
        f_ini.write(f"output = tCl,pCl,lCl,mPk\n")
        f_ini.write(f"background_verbose = 1\n")
        f_ini.write(f"thermodynamics_verbose = 1\n")

    # 2. 実行
    cmd = ["./class", "my_theory.ini"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout
    
    # 3. 数値の抽出（検索ワードを少し広くします）
    rs = "N/A"
    theta = "N/A"
    for line in out.split("\n"):
        if "comoving sound horizon rs =" in line:
            rs = line.split("=")[1].strip().split(" ")[0]
        elif "100*theta_s =" in line:
            theta = line.split("=")[1].strip()
    
    # デバッグ用：もしN/Aならエラーが出ているはずなので、最初の1回だけ中身を確認する指示
    if rs == "N/A" and f == f_list[0]:
        print("--- CLASS Error Log (First Run) ---")
        print(out[:500]) # 冒頭500文字だけ表示
        print("----------------------------------")
    
    print(f"{f:10.3f} | {rs:>12} | {theta:>12}")

print("-" * 45)
