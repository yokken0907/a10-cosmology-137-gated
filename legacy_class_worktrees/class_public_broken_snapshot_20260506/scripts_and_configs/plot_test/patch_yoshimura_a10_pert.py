import os

def insert_code(filepath, marker, injection, offset=0):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    out = []
    done = False
    for i, line in enumerate(lines):
        out.append(line)
        if marker in line and not done:
            out.insert(len(out) + offset, injection + "\n")
            done = True
    if done:
        with open(filepath, 'w') as f:
            f.writelines(out)
        print(f"【成功】 {filepath} に摂動パッチを適用しました。")
    else:
        print(f"【エラー】 {filepath} にマーカーが見つかりません: {marker.strip()}")

# 1. input.c への wy の追加 (疑似真空用パラメータ)
insert_code("source/input.c", "class_read_double(\"yosh_wx\", pba->yosh_wx);", """
  class_read_double("yosh_wy", pba->yosh_wy);
""")
insert_code("include/background.h", "double yosh_wx;", "  double yosh_wy;")

# 2. perturbations.h への変数登録
insert_code("include/perturbations.h", "int index_pt_ur3;", """
  // Yoshimura A10 Model Perturbations
  int index_pt_delta_y;
  int index_pt_theta_y;
  int index_pt_delta_x;
  int index_pt_theta_x;
""")

# 3. perturbations.c : インデックスの割り当て
insert_code("source/perturbations.c", "if (pba->has_ur == _TRUE_) {", """
  if (pba->has_yosh_x == _TRUE_) {
    ppt->index_pt_delta_y = index_pt; index_pt++;
    ppt->index_pt_theta_y = index_pt; index_pt++;
    ppt->index_pt_delta_x = index_pt; index_pt++;
    ppt->index_pt_theta_x = index_pt; index_pt++;
  }
""", offset=-1)

# 4. perturbations.c : 初期条件（ゼロスタート）
insert_code("source/perturbations.c", "if (pba->has_fld == _TRUE_) {", """
  if (pba->has_yosh_x == _TRUE_) {
    y[ppt->index_pt_delta_y] = 0.0;
    y[ppt->index_pt_theta_y] = 0.0;
    y[ppt->index_pt_delta_x] = 0.0;
    y[ppt->index_pt_theta_x] = 0.0;
  }
""", offset=-1)

# 5. perturbations.c : 微分方程式の実装 (perturb_derivs内)
derivs_code = """
  if (pba->has_yosh_x == _TRUE_) {
    double delta_y = y[ppt->index_pt_delta_y];
    double theta_y = y[ppt->index_pt_theta_y];
    double delta_x = y[ppt->index_pt_delta_x];
    double theta_x = y[ppt->index_pt_theta_x];

    double w_y  = pba->yosh_wy; 
    double cs2_y = 1.0;
    double ca2_y = w_y;

    double w_x  = pba->yosh_wx;
    double cs2_x = 1.0;
    double ca2_x = 1.0;

    double hp = pvecmetric[ppw->index_mt_h_prime];
    double Hc = pvecback[pba->index_bg_a] * pvecback[pba->index_bg_H];
    
    double u = log(pvecback[pba->index_bg_a] / pba->yosh_a_star);
    double eps = pba->yosh_gamma_star * exp(-0.5 * u*u / (pba->yosh_sigma_star * pba->yosh_sigma_star));
    double rho_y = pvecback[pba->index_bg_rho_y];
    double rho_x = pvecback[pba->index_bg_rho_x];
    
    // Qc = a * Q = a * H * eps * rho_y = Hc * eps * rho_y
    double Qc = Hc * eps * rho_y; 

    // Y fluid (Quasi-vacuum)
    dy[ppt->index_pt_delta_y] = -(1.0 + w_y) * (theta_y + 0.5 * hp)
                              - 3.0 * Hc * (cs2_y - w_y) * delta_y
                              - 9.0 * Hc * Hc * (1.0 + w_y) * (cs2_y - ca2_y) * theta_y / (k*k);
    dy[ppt->index_pt_theta_y] = - Hc * (1.0 - 3.0 * cs2_y) * theta_y
                              + cs2_y / (1.0 + w_y) * (k*k) * delta_y
                              + Qc / ((1.0 + w_y) * rho_y) * theta_y;

    // X fluid (Stiff/Daughter)
    double Qc_rho_x = (rho_x > 1e-30) ? (Qc / rho_x) : 0.0; // ゼロ割り防止
    dy[ppt->index_pt_delta_x] = -(1.0 + w_x) * (theta_x + 0.5 * hp)
                              - 3.0 * Hc * (cs2_x - w_x) * delta_x
                              + Qc_rho_x * (delta_y - delta_x);
    dy[ppt->index_pt_theta_x] = - Hc * (1.0 - 3.0 * cs2_x) * theta_x
                              + cs2_x / (1.0 + w_x) * (k*k) * delta_x
                              - Qc / ((1.0 + w_x) * rho_x + 1e-30) * theta_x;
  }
"""
insert_code("source/perturbations.c", "if (pba->has_ur == _TRUE_) {", derivs_code, offset=-1)

# 6. perturbations.c : アインシュタイン方程式（重力源）への追加
einstein_code = """
  if (pba->has_yosh_x == _TRUE_) {
    double rho_y = pvecback[pba->index_bg_rho_y];
    double rho_x = pvecback[pba->index_bg_rho_x];
    double delta_y = y[ppt->index_pt_delta_y];
    double theta_y = y[ppt->index_pt_theta_y];
    double delta_x = y[ppt->index_pt_delta_x];
    double theta_x = y[ppt->index_pt_theta_x];
    double w_y = pba->yosh_wy;
    double w_x = pba->yosh_wx;

    *delta_rho += rho_y * delta_y + rho_x * delta_x;
    *delta_p   += 1.0 * rho_y * delta_y + 1.0 * rho_x * delta_x; // cs2 = 1.0
    *rho_plus_p_theta += (1.0 + w_y) * rho_y * theta_y + (1.0 + w_x) * rho_x * theta_x;
  }
"""
insert_code("source/perturbations.c", "/* scalar field */", einstein_code, offset=-1)
