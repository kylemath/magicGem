arXiv Submission Package for "Magic Gems: A Polyhedral Framework for Magic Squares"
====================================================================================

This folder contains all files necessary for submission to arXiv.

FILES INCLUDED:
--------------
- main.tex              : Main LaTeX document
- references.bib        : Bibliography file (arXiv will compile this)
- sections/             : All LaTeX section files
- figures/              : All figure files referenced in the document
- anc/                  : Ancillary files (code/data)
  - analysis_code.zip   : Zipped source code (scripts/ and src/)

SUBMISSION INSTRUCTIONS:
------------------------
1. Go to https://arxiv.org/submit
2. Log in with your arXiv account
3. Start a new submission
4. Fill in the submission metadata (see ARXIV_FORM_FIELDS.txt)
5. Upload all files in this directory:
   - main.tex
   - references.bib
   - sections/ (folder)
   - figures/ (folder)
   - anc/ (folder) - arXiv will treat files in 'anc' as supplementary material
6. arXiv will automatically compile the LaTeX and generate the PDF
7. Review the compiled PDF and submit

IMPORTANT NOTES:
----------------
- **Code:** Your analysis code is included in 'anc/analysis_code.zip'. arXiv automatically serves files in the 'anc' directory as supplementary material.
- **Web App:** An interactive Magic Gem visualization is available at https://kylemath.github.io/MagicGemWebpage/ and is referenced in the paper.
- **Reviewers:** A list of suggested reviewers (math/stats experts) is in SUGGESTED_REVIEWERS.txt.

VERIFICATION CHECKLIST:
-----------------------
See PRE_SUBMISSION_CHECKLIST.txt for a detailed check.

CONTACT:
--------
Kyle Elliott Mathewson
Faculty of Science, University of Alberta
kyle.mathewson@ualberta.ca
