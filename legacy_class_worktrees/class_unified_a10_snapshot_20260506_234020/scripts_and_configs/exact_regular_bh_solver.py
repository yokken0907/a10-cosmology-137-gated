import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- 物理パラメータの定義 ---
rho_c = 1.0     # 中心密度
r_c = 1.0       # スケール半径
m_idx = 3.0     # 冪指数 m (>=2 で中心正則)
q_idx = 2.0     # 冪指数 q (m*q > 3 でADM質量有限)

# --- 解析的なプロファイル関数 ---
def rho(r):
    """密度プロファイル"""
    return rho_c / (1.0 + (r / r_c)**m_idx)**q_idx

def d_rho_dr(r):
    """密度プロファイルの解析的導関数 (dρ/dr)"""
    num = -rho_c * q_idx * m_idx * (r / r_c)**(m_idx - 1)
    den = r_c * (1.0 + (r / r_c)**m_idx)**(q_idx + 1)
    return num / den

def p_r(r):
    """動径圧力 (状態方程式 p_r = -ρ を要請)"""
    return -rho(r)

def p_t(r):
    """接線圧力 (エネルギー保存則より解析的に導出)"""
    return -rho(r) - (r / 2.0) * d_rho_dr(r)

# --- 質量関数 m(r) の常微分方程式 ---
def mass_equation(r, y):
    m = y[0]
    dm_dr = 4 * np.pi * r**2 * rho(r)
    return [dm_dr]

# 事象の地平面 f(r) = 1 - 2m/r = 0 を検出するためのイベント関数
def horizon_event(r, y):
    m = y[0]
    return r - 2 * m
horizon_event.direction = 0

# --- 積分設定 ---
r_start = 1e-8
r_end = 20.0
m_0 = [4/3 * np.pi * r_start**3 * rho(r_start)]

# ODE求解
sol_m = solve_ivp(
    mass_equation, 
    [r_start, r_end], 
    m_0, 
    events=horizon_event, 
    dense_output=True, 
    method='Radau'
)

# 評価用配列
r_arr = np.linspace(r_start, r_end, 2000)
m_arr = sol_m.sol(r_arr)[0]

# --- 従属変数の計算 ---
# 計量関数 f(r)
f_arr = 1.0 - 2.0 * m_arr / r_arr
# 中心 r->0 の極限は f(0) = 1 (de Sitterコア)
f_arr[r_arr < 1e-7] = 1.0 

rho_arr = rho(r_arr)
pr_arr = p_r(r_arr)
pt_arr = p_t(r_arr)

# エネルギー条件の評価パラメータ
rho_plus_pt = rho_arr + pt_arr               # NEC/WEC (tangential) の判定
rho_plus_pr_plus_2pt = -2*rho_arr - r_arr*d_rho_dr(r_arr) # SEC の判定

# --- コンソール出力: 地平面とADM質量の検証 ---
print("=== メタ妥当性評価: Exact Solution Model ===")
M_ADM = m_arr[-1]
print(f"ADM Mass (M) at r={r_end}: {M_ADM:.6f}")

if len(sol_m.t_events[0]) > 0:
    for i, r_h in enumerate(sol_m.t_events[0]):
        print(f"Horizon [{i+1}] detected at r_h = {r_h:.6f}")
else:
    print("No event horizon detected (Regular Compact Object).")

# --- プロットの生成 ---
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# 1. 物質プロファイルと圧力
axs[0].plot(r_arr, rho_arr, label=r'$\rho$ (Density)', color='black', linewidth=2)
axs[0].plot(r_arr, pr_arr, label=r'$p_r = -\rho$', color='blue', linestyle='--')
axs[0].plot(r_arr, pt_arr, label=r'$p_t = -\rho - \frac{r}{2}\rho^\prime$', color='red', linestyle='-.')
axs[0].set_xlabel('Radius r')
axs[0].set_ylabel('Density / Pressure')
axs[0].set_title('Anisotropic Fluid Profiles')
axs[0].legend()
axs[0].grid(True)

# 2. 計量関数 f(r) と事象の地平面
axs[1].plot(r_arr, f_arr, label=r'$f(r) = 1 - 2m(r)/r$', color='purple', linewidth=2)
axs[1].axhline(0, color='black', linestyle='-', linewidth=0.8)
if len(sol_m.t_events[0]) > 0:
    for r_h in sol_m.t_events[0]:
        axs[1].axvline(r_h, color='red', linestyle=':', label=f'Horizon $r_h={r_h:.2f}$')
axs[1].set_xlabel('Radius r')
axs[1].set_ylabel('Metric Function f(r)')
axs[1].set_title('Metric Function & Horizons')
axs[1].legend()
axs[1].grid(True)
axs[1].set_ylim(-0.5, 1.2)

# 3. エネルギー条件 (Energy Conditions)
axs[2].plot(r_arr, rho_plus_pt, label=r'$\rho + p_t$ (Tangential NEC/WEC)', color='green')
axs[2].plot(r_arr, rho_plus_pr_plus_2pt, label=r'$\rho + p_r + 2p_t$ (SEC)', color='orange')
axs[2].axhline(0, color='black', linestyle='-', linewidth=0.8)
axs[2].set_xlabel('Radius r')
axs[2].set_ylabel('Energy Condition Scalars')
axs[2].set_title('Energy Conditions Diagnostic')
axs[2].legend()
axs[2].grid(True)
# SECの破れ（負の領域）を視覚化するため表示範囲を調整
axs[2].set_ylim(min(np.min(rho_plus_pr_plus_2pt), -1.5), max(np.max(rho_plus_pt), 1.0))

plt.tight_layout()
output_filename = 'exact_regular_bh_diagnostics.png'
plt.savefig(output_filename)
print(f"\nDiagnostic plot saved successfully as {output_filename}")