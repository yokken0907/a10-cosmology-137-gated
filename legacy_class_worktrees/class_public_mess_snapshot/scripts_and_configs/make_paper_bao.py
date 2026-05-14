import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    # 評価する赤方偏移 (BOSS DR12)
    z = np.array([0.38, 0.51, 0.61])

    # BOSS DR12 観測データ (D_M / r_d)
    data_dm_rs = np.array([10.23, 13.36, 15.45])
    data_err = np.array([0.17, 0.21, 0.22])

    # 先ほど算出した理論値
    std_dm_rs = np.array([10.4283, 13.5065, 15.7146])
    a10_dm_rs = np.array([9.9843, 12.9730, 15.1284])
    
    # A10モデルの観測に対するズレ (何σか)
    a10_sigma = np.abs(a10_dm_rs - data_dm_rs) / data_err

    # ==========================================
    # 1. 論文用グラフ (Figure 4) の生成
    # ==========================================
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 標準モデル (黒点線)
    ax.plot(z, std_dm_rs, 'k--', marker='s', markersize=6, alpha=0.6, label=r'Standard $\Lambda$CDM ($h=0.67$)')
    
    # A10モデル (水色実線)
    ax.plot(z, a10_dm_rs, 'c-', marker='o', markersize=8, lw=2, label=r'A10 Model ($H_0=72$)')
    
    # BOSS観測データ (赤色エラーバー)
    ax.errorbar(z, data_dm_rs, yerr=data_err, fmt='ro', markersize=8, capsize=5, capthick=2, elinewidth=2, label='BOSS DR12 Data')
    
    ax.set_xlabel('Redshift $z$', fontsize=14)
    ax.set_ylabel(r'BAO Observable $D_M / r_d$', fontsize=14)
    ax.set_title('Late-Time Constraints: BAO Measurements (BOSS DR12)', fontsize=15)
    
    # 軸の範囲と見た目の調整
    ax.set_xlim(0.35, 0.65)
    ax.set_xticks([0.38, 0.51, 0.61])
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('Figure_4_BAO.png', dpi=300)
    plt.close()

    # ==========================================
    # 2. 論文用 LaTeX テーブルの出力
    # ==========================================
    latex_table = f"""
\\begin{{table}}[h]
\\centering
\\begin{{tabular}}{{lcccc}}
\\hline\\hline
Redshift $z$ & BOSS DR12 & $\\Lambda$CDM & A10 Model & Tension ($\\sigma$) \\\\
\\hline
0.38 & $10.23 \\pm 0.17$ & 10.43 & {a10_dm_rs[0]:.2f} & {a10_sigma[0]:.2f} \\\\
0.51 & $13.36 \\pm 0.21$ & 13.51 & {a10_dm_rs[1]:.2f} & {a10_sigma[1]:.2f} \\\\
0.61 & $15.45 \\pm 0.22$ & 15.71 & {a10_dm_rs[2]:.2f} & {a10_sigma[2]:.2f} \\\\
\\hline\\hline
\\end{{tabular}}
\\caption{{Comparison of the BAO observable $D_M/r_d$ between the standard $\\Lambda$CDM model, the A10 model, and observational data from BOSS DR12. The deviation of the A10 model remains within $\\sim 1.8\\sigma$, representing a mild trade-off to resolve the Hubble tension.}}
\\label{{tab:bao_comparison}}
\\end{{table}}
"""
    print("✅ 論文用の画像『Figure_4_BAO.png』を作成しました！")
    print("✅ 論文(.texファイル)にそのままコピペできる LaTeX コードを出力します：\n")
    print(latex_table)

if __name__ == '__main__':
    main()