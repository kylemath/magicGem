# Magic Square Gems – Submission to *Mathematics* (MDPI)

> Working directory: `/magicSquare/submissionToMathematics`

This README serves as the **central checklist and integration guide** for preparing our manuscript _"Geometric and Topological Analysis of Magic Squares"_ (and its planned companion work on vector‐field representations) for submission to the Q1 open–access journal **Mathematics** (ISSN 2227-7390, MDPI).

---
## 1 Current Assets in the Repository

| Path | Content | Notes |
|------|---------|-------|
| `magic_squares/` | Core Python package, dataset loader, LaTeX source (`tex/`) of the first manuscript, plus helper scripts | **Stable** foundation of the geometric/EMD/persistence analysis. |
| `figures_manifold/` | Interactive t-SNE and other 3-D manifold HTML plots | Generated via Plotly; useful for supplementary material. |
| `spinning_top/` | Prototype code for **vector-emission model** (treating each square entry as a radial beam); includes early Three.js visualisations | Will form the nucleus of Paper 2 & supplementary demo. |
| `axial_shape/` | Experiments on axial symmetry & hull metrics | To be merged into Methods → Hull metrics subsection. |
| `covariance_proof/` | Draft notes proving zero-covariance of the vector-field embedding | Needs polishing & integration into theoretical results. |
| `magic_squares.egg-info/`, `venv/` | Build artefacts / local virtual-env | _Exclude from the final submission zip_. |
| `requirements.txt` | Minimal run-time dependencies | Eventually mirror into an `environment.yml` for Binder. |

---
## 2 What *this* Folder Will Contain

* `README.md` (this file)
* `submission.tex` → cleaned & MDPI-compliant master manuscript
* `figures/`    → high-resolution (300 dpi) PNG + native PDF/PGF figures
* `supplementary/` → interactive HTML, Jupyter notebooks, raw datasets
* `code_zip/`      → reproducibility snapshot (scripts + data under 50 MB)

(*Empty placeholders will be committed as we progress.*)

---
## 3 Outstanding Tasks / To-Do List

### A. Scientific Content
1. **Vector-Field Representation**
   * ✅ Formalise definition (position, azimuth, magnitude mapping).
   * ✅ Complete zero-covariance proof & connect to balancing intuition.
   * ✅ Compute comparable persistence & EMD statistics; contrast with R³ embedding.
2. **Manifold Comparison**
   * ✅ Extend t-SNE/UMAP to include perturbed & "near-magic" squares.
   * ✅ Quantify separation between true magic manifold and perturbed cloud.
3. **Additional Theorems**
   * ✅ Prove dimensionality claim `d = n² − 2n` formally (add to Section 3).
   * ✅ Provide algorithmic complexity analysis for the dual-null pipeline.
4. **Results Integration**
   * ✅ Update LaTeX sections (Methods, Results, Discussion) with new metrics.
   * ✅ Add figure panels: convex-hull facets colouring, spinning-top snapshots.
5. **Broader Applications Paragraph** (coding theory, quantum info, etc.).
   * ✅ Broader Applications Paragraph (coding theory, quantum info, etc.).

### B. Reproducibility & Supplementary Material
1. Clean notebooks; convert heavy interactive plots to lightweight HTML.
2. ✅ Prepare `run_all.py` that rebuilds every figure from raw CSV.
3. ✅ Provide Dockerfile or conda `environment.yml` for reviewers.

### C. Manuscript & Submission Logistics
1. ✅ Switch to MDPI `article` template (`mdpi.cls`) — adjust metadata.
2. ✅ Ensure citation style = *Mathematics* (numeric). Check DOIs.
3. ✅ Compress figures to meet MDPI size limits (< 20 MB total).
4. ✅ Draft cover letter referencing Feature Paper invitation and fee waiver.
5. ✅ Generate *Highlights* (3 × 85 characters) & *Graphical Abstract*.
6. ✅ Proof-read for jargon; tighten abstract (< 200 words recommended).
7. ✅ Run TeX lint & compile under TeXLive 2023 (report warnings).
8. ✅ Internal co-author review loop → iterate until "ready to submit".

### D. Nice-to-Haves (time permitting)
* Live Binder / Colab link for interactive exploration.
* Short video (≤ 30 s) rotating the magic-gem polytope for social media.

---
## 4 Timeline (tentative)
| Week | Milestone |
|------|-----------|
| W1   | ✅ Finish zero-covariance proof; integrate into LaTeX |
| W2   | ✅ Generate new vector-field figures & statistics |
| W3   | ✅ Re-format manuscript to MDPI template; internal review |
| W4   | ✅ Final polish, cover letter, upload to Mathematics MDPI |

---
**✅ SUBMISSION PACKAGE COMPLETE**

> _"Balanced numbers, balanced code, balanced prose."_ – Project mantra 