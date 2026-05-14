import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# 出力ディレクトリ作成
if not os.path.exists("output"):
    os.makedirs("output")

# --- 1. 二つの宇宙の設定ファイルを作成 ---

# 標準モデル (LCDM)
with open("lcdm_std.ini", "w") as f:
    f.write("""
H0 = 67.36
Omega_b = 0.0493
Omega_cdm = 0.264
n_s = 0.9665
A_s = 2.105e-9
tau_reio = 0.0544
output = tCl,pCl,lCl
root = output/std_
""")

# 吉村モデル (A1)
with open("yoshimura.ini", "w") as f:
    f.write("""
H0 = 72.6397
Omega_b = 0.0486
Omega_cdm = 0.2589
z_star_yoshimura = 3000.0
f_star_yoshimura = 0.135
n_s = 0.9665
A_s = 2.105e-9
tau_reio = 0.0544
output = tCl,pCl,lCl
root = output/yoshi_
""")

# --- 2. CLASSを実行 ---
print("計算中: 標準モデル...")
subprocess.run(["./class", "lcdm_std.ini"], capture_output=True)
print("計算中: 吉村モデル...")
subprocess.run(["./class", "yoshimura.ini"], capture_output=True)

# --- 3. データの読み込み ---
def load_cl(path):
    if os.path.exists(path):
        data = np.loadtxt(path)
        return data[:, 0], data[:, 1] # l, TT
    return None, None

l_std, tt_std = load_cl("output/std_cl.dat")
l_yoshi, tt_yoshi = load_cl("output/yoshi_cl.dat")

if l_std is not None and l_yoshi is not None:
    plt.figure(figsize=(10, 6))
    plt.plot(l_std, tt_std, label="Standard LCDM ($H_0 \\approx 67$)", color="gray", linestyle="--")
    plt.plot(l_yoshi, tt_yoshi, label="Yoshimura A1 Model ($H_0 \\approx 73$)", color="red", linewidth=2)

    plt.xlabel(r"Multipole $\ell$")
    plt.ylabel(r"$\ell(\ell+1)C_\ell / 2\pi$")
    plt.title("Comparison of CMB Power Spectra")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(2, 2500)
    plt.savefig("yoshimura_comparison.png")
    print("\n【祝・大成功】 'yoshimura_comparison.png' を作成しました！")
else:
    print("\n【エラー】ファイルが生成されませんでした。")
