import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- 物理パラメータの定義 ---
rho_c = 1.0     
r_c = 1.0       
m_idx = 2.0     
q_idx = 2.0     
r_t = 1.5       
s_idx = 2.0     

# --- 解析的なプロファイル関数 ---
def rho(r):
    return rho_c / (1.0 + (r / r_c)**m_idx)**q_idx

def p_r(r):
    return -rho(r) * np.exp(-(r / r_t)**s_idx)

# --- 質量関数 m(r) の独立した常微分方程式 ---
def mass_equation(r, y):
    m = y[0]
    dm_dr = 4 * np.pi * r**2 * rho(r)
    return [dm_dr]

# 事象の地平面 r = 2m(r) を検出するためのイベント関数
def horizon_event(r, y):
    m = y[0]
    return r - 2 * m
horizon_event.direction = 0  # 交差の方向を問わない

# --- 積分設定 ---
r_start = 1e-5
r_end = 20.0
m_0 = [4/3 * np.pi * r_start**3 * rho(r_start)]

# --- 質量関数の積分実行 ---
sol_m = solve_ivp(
    mass_equation, 
    [r_start, r_end], 
    m_0, 
    events=horizon_event, 
    dense_output=True, 
    method='Radau'
)

# 評価用配列の生成と解の取得
r_eval = np.linspace(r_start, r_end, 2000)
m_eval = sol_m.sol(r_eval)[0]

# --- 正則性条件の評価 ---
print("=== メタ妥当性評価: 地平面における正則性の検証 ===")
if len(sol_m.t_events[0]) > 0:
    for i, r_h in enumerate(sol_m.t_events[0]):
        m_h = sol_m.y_events[0][i][0]
        pr_h = p_r(r_h)
        
        # 正則性条件の残差計算: m(r_h) + 4 * pi * r_h^3 * p_r(r_h)
        residual = m_h + 4 * np.pi * r_h**3 * pr_h
        
        print(f"Horizon [{i+1}]: r_h = {r_h:.6f}")
        print(f"  m(r_h) = {m_h:.6f}")
        print(f"  p_r(r_h) = {pr_h:.6f}")
        print(f"  Regularity Residual = {residual:.6e}")
        
        if abs(residual) < 1e-5:
            print("  [判定] 正則性条件は満たされています。Phi(r)の積分が可能です。")
        else:
            print("  [判定] 致命的な残差が存在します。現在のパラメータではPhi(r)が発散します。")
else:
    print("事象の地平面は形成されませんでした（星モデル）。")

# --- プロットの生成 (質量関数のみ) ---
plt.figure(figsize=(8, 6))
plt.plot(r_eval, m_eval, label='Mass m(r)', color='black')
plt.plot(r_eval, r_eval / 2.0, label='r/2 (Horizon Condition)', color='gray', linestyle=':')

if len(sol_m.t_events[0]) > 0:
    for r_h, m_h in zip(sol_m.t_events[0], sol_m.y_events[0]):
        plt.scatter(r_h, m_h[0], color='red', zorder=5)
        plt.annotate(f'$r_h={r_h:.3f}$', (r_h, m_h[0]), textcoords="offset points", xytext=(10,-10), ha='center')

plt.xlabel('Radius r')
plt.ylabel('Mass m(r)')
plt.title('Mass Function up to $r=20.0$')
plt.legend()
plt.grid(True)
plt.xlim(0, 2.0)
plt.ylim(0, 1.0)
plt.tight_layout()
plt.savefig('mass_function_full.png')
print("\nPlot saved successfully as mass_function_full.png")