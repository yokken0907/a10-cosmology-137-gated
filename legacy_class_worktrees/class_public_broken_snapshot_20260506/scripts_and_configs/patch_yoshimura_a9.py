import os

def insert_code(filepath, marker, injection):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    out = []
    done = False
    for line in lines:
        out.append(line)
        if marker in line and not done:
            out.append(injection + "\n")
            done = True
    if done:
        with open(filepath, 'w') as f:
            f.writelines(out)
        print(f"【成功】 {filepath} に A9 物理モデルを組み込みました。")
    else:
        print(f"【警告】 {filepath} にマーカーが見つかりませんでした: {marker.strip()}")

# 1. background.h の書き換え
insert_code("include/background.h", "short has_fld;", """
  short has_yosh_x;
  double yosh_z_star;
  double yosh_a_star;
  double yosh_sigma_star;
  double yosh_gamma_star;
  double yosh_wx;
  double yosh_fY;
  int index_bi_rho_y;
  int index_bi_rho_x;
  int index_bg_rho_y;
  int index_bg_rho_x;
  int index_bg_p_y;
  int index_bg_p_x;
""")

# 2. input.c の書き換え
insert_code("source/input.c", "class_read_double(\"Omega_fld\",pba->Omega0_fld);", """
  class_read_int("has_yosh_x", pba->has_yosh_x);
  class_read_double("yosh_z_star", pba->yosh_z_star);
  class_read_double("yosh_sigma_star", pba->yosh_sigma_star);
  class_read_double("yosh_gamma_star", pba->yosh_gamma_star);
  class_read_double("yosh_wx", pba->yosh_wx);
  class_read_double("yosh_fY", pba->yosh_fY);
  if (pba->has_yosh_x == _TRUE_) {
    pba->yosh_a_star = 1.0 / (1.0 + pba->yosh_z_star);
  }
""")

# 3. background.c の書き換え (複数箇所)
bg_file = "source/background.c"
insert_code(bg_file, "pba->index_bg_H = index_bg;", """
  if (pba->has_yosh_x == _TRUE_) {
    pba->index_bg_rho_y = index_bg; index_bg++;
    pba->index_bg_rho_x = index_bg; index_bg++;
    pba->index_bg_p_y = index_bg; index_bg++;
    pba->index_bg_p_x = index_bg; index_bg++;
  }
""")

insert_code(bg_file, "pba->index_bi_time = index_bi;", """
  if (pba->has_yosh_x == _TRUE_) {
    pba->index_bi_rho_y = index_bi; index_bi++;
    pba->index_bi_rho_x = index_bi; index_bi++;
  }
""")

insert_code(bg_file, "pvecback_integration[pba->index_bi_time] = a/(pba->H0*sqrt(pba->Omega0_r));", """
  if (pba->has_yosh_x == _TRUE_) {
    pvecback_integration[pba->index_bi_rho_x] = 0.0;
    double a_star = pba->yosh_a_star;
    double rho_r_star = pba->Omega0_g * pow(a_star,-4) + pba->Omega0_ur * pow(a_star,-4);
    double rho_m_star = pba->Omega0_b * pow(a_star,-3) + pba->Omega0_cdm * pow(a_star,-3);
    pvecback_integration[pba->index_bi_rho_y] = pba->yosh_fY * (rho_r_star + rho_m_star);
  }
""")

insert_code(bg_file, "dy[pba->index_bi_time] = 1./(a*H);", """
  if (pba->has_yosh_x == _TRUE_) {
    double u = log(a / pba->yosh_a_star);
    double eps = pba->yosh_gamma_star * exp(-0.5 * u * u / (pba->yosh_sigma_star * pba->yosh_sigma_star));
    dy[pba->index_bi_rho_y] = -eps * y[pba->index_bi_rho_y];
    dy[pba->index_bi_rho_x] = -3.0 * (1.0 + pba->yosh_wx) * y[pba->index_bi_rho_x] + eps * y[pba->index_bi_rho_y];
  }
""")

insert_code(bg_file, "if (pba->has_fld == _TRUE_) {", """
  if (pba->has_yosh_x == _TRUE_) {
    pvecback_B[pba->index_bg_rho_y] = pvecback_integration[pba->index_bi_rho_y];
    pvecback_B[pba->index_bg_rho_x] = pvecback_integration[pba->index_bi_rho_x];
    pvecback_B[pba->index_bg_p_y]   = -pvecback_B[pba->index_bg_rho_y];
    pvecback_B[pba->index_bg_p_x]   = pba->yosh_wx * pvecback_B[pba->index_bg_rho_x];
    *rho_tot += pvecback_B[pba->index_bg_rho_y] + pvecback_B[pba->index_bg_rho_x];
    *p_tot   += pvecback_B[pba->index_bg_p_y]   + pvecback_B[pba->index_bg_p_x];
  }
""")
