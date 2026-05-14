Goal:
  Determine whether has_unified_a10 activates non-vanishing dynamics even when ua10_V0 = 0.

Read in this order:
  1) input_parser_defaults_focus.txt
  2) background.focused_windows.txt
  3) background.without_ua10_V0.txt
  4) perturbations.focused_windows.txt
  5) perturbations.without_ua10_V0.txt

What to flag:
  - any term inside a has_unified_a10 branch that does not multiply ua10_V0
  - any background or perturbation source added solely by has_unified_a10
  - any initial-condition change triggered by has_unified_a10 regardless of ua10_V0

Interpretation:
  - If such terms exist, unified is not a zero-amplitude limit of legacy A10.
  - If no such terms exist, investigate normalization, units, or solver stiffness next.
