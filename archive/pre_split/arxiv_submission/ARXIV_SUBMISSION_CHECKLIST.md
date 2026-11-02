# arXiv submission checklist for v5 (arXiv:2512.09170v5)

## Files to upload
- `main.tex`
- `sections/abstract.tex`, `introduction.tex`, `background.tex`, `gem.tex`, `theory.tex`, `computations.tex`, `discussion.tex`, `conclusion.tex`, `appendix.tex`
  (NOT needed: `sections/witnesses.tex` — no longer input; `sections/drafts/` — not input)
- `references.bib` and `main.bbl` (arXiv runs pdflatex but not bibtex; the `.bbl` from the final clean compile must be uploaded)
- Figures actually included (vector PDF):
  - `figures/fig01_construction_d4.pdf` (Fig. 1)
  - `figures/fig_random_energy.pdf` (Fig. 2)
  - `figures/fig_gem_geometry_880.pdf` (Fig. 3)
  - `figures/fig_siamese_layers.pdf` (Fig. 4)
  (NOT included, do not upload: `fig02_combined_construction_symmetries.pdf`, `fig03_combined_3x3_analysis.pdf`, `fig_lowmode_gallery.pdf`, `fig_lowmode_vs_full_n4.pdf`, `fig_gems_cross_order.pdf`)
- Ancillary: `anc/analysis_code.zip` (contains `analysis_code/src`, `revision/`, `revision_round1/`, `revision_round2/appendix_data.json|.md`, README, requirements, the 880-square array)

Do not upload: `main.aux`, `main.log`, `main.out`, `main.blg`, `main.pdf`, `magicGemV5.pdf`, `CHANGES_V5.md`, `REVISION_PLAN_V5.md`, `review_confidential.md`, `review_rounds/`, this checklist.

## Suggested arXiv "Comments" field
`v5: major revision after review. Corrects v4 (asymmetric energy, sampled statistics, swap-gap structure, rarity estimate; see Section 1, "Corrections relative to version 4"). 27 pages, 4 figures, 4 tables; ancillary files contain all code and data (CHANGES_V5.md in the repository lists every change).`

## Before uploading
1. Copy only the files above into a **fresh, empty directory** and run there, with the basic TeX Live used for the manuscript:
   `pdflatex main && bibtex main && pdflatex main && pdflatex main`
   Expect: 27 pages, no errors, no undefined references or citations, no Type 3 fonts (`pdffonts main.pdf`).
2. Upload the freshly produced `main.bbl` from that directory (not an older one).
3. arXiv's `\today` in `\date{}` will stamp the compile date; replace by a fixed date if a specific date is wanted.
4. The arXiv abstract field must be plain text: paste the abstract without `\Cov`, `\emph` and `$...$` where possible (arXiv accepts simple TeX math).
5. Check the arXiv-produced PDF once for the four figures and the in-flow Table 2 on p. 18.
