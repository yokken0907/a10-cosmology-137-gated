import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 視覚的疲労を軽減するための背景色設定
plt.style.use('dark_background')

# --- 物理パラメータの定義 ---
rho_c = 1.0
r_c = 1.0
m_idx = 3.0
q_idx = 2.0

# --- 解析的なプロファイル関数 ---
def rho(r):
    return rho_c / (1.0 + (r / r_c)**m_idx)**q_idx

def d_rho_dr(r):
    num = -rho_c * q_idx * m_idx * (r / r_c)**(m_idx - 1)
    den = r_c * (1.0 + (r / r_c)**m_idx)**(q_idx + 1)
    return num / den

def mass_equation(r, y):
    m = y[0]
    dm_dr = 4 * np.pi * r**2 * rho(r)
    return [dm_dr]

# --- 積分設定 ---
r_start = 1e-8
r_end = 20.0
m_0 = [4/3 * np.pi * r_start**3 * rho(r_start)]

sol_m = solve_ivp(mass_equation, [r_start, r_end], m_0, dense_output=True, method='Radau')

r_arr = np.linspace(r_start, r_end, 2000)
m_arr = sol_m.sol(r_arr)[0]
rho_arr = rho(r_arr)
d_rho_dr_arr = d_rho_dr(r_arr)

# --- 曲率不変量の解析的計算 ---
# 1. リッチスカラー R
R_arr = 8.0 * np.pi * (4.0 * rho_arr + r_arr * d_rho_dr_arr)

# 2. リッチテンソル二乗 R_mu_nu R^mu^nu
R_sq_arr = 128.0 * np.pi**2 * ((rho_arr + 0.5 * r_arr * d_rho_dr_arr)**2 + rho_arr**2)

# 3. クレッチマンスカラー K
# ゼロ除算を回避するため r_arr の極小値に対する処理を含む
term1 = -4.0 * m_arr / r_arr**3 - 8.0 * np.pi * r_arr * d_rho_dr_arr
term2 = 2.0 * m_arr / r_arr**3 - 8.0 * np.pi * rho_arr
term3 = 2.0 * m_arr / r_arr**3

K_arr = term1**2 + 4.0 * term2**2 + 4.0 * term3**2

# --- 理論的極限値 (r -> 0) のコンソール出力 ---
R_0 = 32.0 * np.pi * rho_c
R_sq_0 = 256.0 * np.pi**2 * rho_c**2
K_0 = (512.0 / 3.0) * np.pi**2 * rho_c**2

print("=== 曲率不変量の中心極限 (r -> 0) 理論値 ===")
print(f"R(0) = {R_0:.4f}")
print(f"R_mu_nu R^mu^nu(0) = {R_sq_0:.4f}")
print(f"K(0) = {K_0:.4f}")
print("============================================")

# --- プロットの生成 ---
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# リッチスカラー R
axs[0].plot(r_arr, R_arr, color='cyan', linewidth=2)
axs[0].axhline(R_0, color='white', linestyle=':', label=r'Theoretical $R(0)$')
axs[0].set_xlabel('Radius r')
axs[0].set_ylabel(r'Ricci Scalar $R$')
axs[0].set_title('Ricci Scalar')
axs[0].legend()
axs[0].grid(True, alpha=0.3)

# リッチテンソル二乗
axs[1].plot(r_arr, R_sq_arr, color='magenta', linewidth=2)
axs[1].axhline(R_sq_0, color='white', linestyle=':', label=r'Theoretical $R_{\mu\nu}R^{\mu\nu}(0)$')
axs[1].set_xlabel('Radius r')
axs[1].set_ylabel(r'$R_{\mu\nu}R^{\mu\nu}$')
axs[1].set_title('Ricci Squared')
axs[1].legend()
axs[1].grid(True, alpha=0.3)

# クレッチマンスカラー
axs[2].plot(r_arr, K_arr, color='yellow', linewidth=2)
axs[2].axhline(K_0, color='white', linestyle=':', label=r'Theoretical $K(0)$')
axs[2].set_xlabel('Radius r')
axs[2].set_ylabel(r'Kretschmann Scalar $K$')
axs[2].set_title('Kretschmann Scalar')
axs[2].legend()
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
output_filename = 'curvature_invariants.png'
plt.savefig(output_filename)
print(f"\nPlot saved successfully as {output_filename}")