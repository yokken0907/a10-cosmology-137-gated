#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-$PWD}"
cd "$ROOT"
TEX="repaired_unified_a10_followup_v6.tex"

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode "$TEX"
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode "$TEX"
  pdflatex -interaction=nonstopmode "$TEX"
else
  echo "Neither latexmk nor pdflatex was found."
  echo "On Ubuntu/WSL, install a TeX distribution with:"
  echo "  sudo apt update"
  echo "  sudo apt install -y latexmk texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-science lmodern"
  exit 127
fi
