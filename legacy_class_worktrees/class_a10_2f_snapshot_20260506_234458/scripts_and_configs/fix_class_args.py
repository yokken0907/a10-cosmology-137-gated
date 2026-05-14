with open('a10_2f_ef.yaml', 'r') as f:
    text = f.read()

# extra_args の下にある余分な改行や設定を整理し、
# Planck データが要求する厳密な解像度設定を追加する
if "N_ur: 2.0328" not in text:
    old_args = """    extra_args:
      has_a10_2f: 'yes'
      Omega_fld: 1e-5
      a10_npost: 2.0
      a10_xi137: 137.036
      a10_gamma0: 0.0
      a10_cs_model: 1
      lensing: 'yes'"""
      
    new_args = """    extra_args:
      has_a10_2f: 'yes'
      Omega_fld: 1e-5
      a10_npost: 2.0
      a10_xi137: 137.036
      a10_gamma0: 0.0
      a10_cs_model: 1
      # --- Planck Requirements ---
      lensing: 'yes'
      N_ur: 2.0328
      N_ncdm: 1
      m_ncdm: 0.06
      T_ncdm: 0.71611
      # 精度設定 (MCMC で発散しないように)
      tol_background_integration: 1e-3
      tol_perturb_integration: 1e-4"""
    
    text = text.replace(old_args, new_args)

with open('a10_2f_ef.yaml', 'w') as f:
    f.write(text)
