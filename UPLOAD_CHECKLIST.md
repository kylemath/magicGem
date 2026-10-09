# arXiv upload checklist: Magic Gems (A) and Moments of Magic Squares (B)

Branch `split-papers-a-b`. Both tarballs build from a clean directory with `pdflatex main; bibtex main; pdflatex main; pdflatex main` and match the committed PDFs.

| | Paper A | Paper B |
|---|---|---|
| Title | Magic Gems: A Polyhedral Framework for Magic Squares | Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies |
| arXiv action | **Replace** arXiv:2512.09170 (becomes v5) | **New submission** |
| PDF | `paper_A_gems/paperA.pdf` (22 pp, 8 figures) | `paper_B_orthogonality/paperB.pdf` (23 pp, 3 figures, 4 tables) |
| Upload file | `paper_A_gems/paperA_arxiv.tar.gz` (776 KB) | `paper_B_orthogonality/paperB_arxiv.tar.gz` (392 KB) |
| Ancillary files | `anc/` at the top of the tarball (65 files) | `anc/` at the top of the tarball (72 files) |
| Metadata text | `paper_A_gems/submission_notes/arxiv_comments.md` | `paper_B_orthogonality/submission_notes/arxiv_metadata.md` |
| Abstract length | 1824 characters (limit 1920) | 1740 characters (limit 1920) |
| Primary category | math.CO | math.CO |
| Cross-lists | math.MG (optional) | math.PR; math.NT (optional) |
| MSC 2020 | 05B15, 52B05, 52B15, 52B20 | 05B20 (primary); 05A05, 11C08, 60C05, 60F05 |

## Order

1. **Read both PDFs once yourself.** Check your name, affiliation and email on page 1. Both use `\today`, so arXiv stamps the date it compiles.
2. **Submit Paper B first, as a new submission.**
   - Upload `paperB_arxiv.tar.gz`. arXiv picks up `anc/` as ancillary files automatically.
   - Paste title, abstract, comments, categories and MSC codes from `arxiv_metadata.md`. The abstract there is in TeX; arXiv accepts `$...$`.
   - Choose a licence (CC BY 4.0 is suggested).
   - Paper B already cites Paper A as arXiv:2512.09170, so it needs no later change.
3. **Wait for Paper B's arXiv number**, then tell Claude. Paper A's bibliography entry `mathewson_companion` currently says "Manuscript"; it should become `arXiv:<B's number>`. This is a one-line change plus a rebuild of the tarball.
4. **Replace arXiv:2512.09170 with Paper A.**
   - Use "Replace", not "New submission", on 2512.09170.
   - Upload the rebuilt `paperA_arxiv.tar.gz`.
   - Use the comments and abstract from `arxiv_comments.md`. The title is unchanged.
   - Ignore the "Candid list" section in that file; it is private notes.
5. **After both are announced:** nothing else is needed. Optionally, update the web app at kylemath.github.io/MagicGemWebpage to link both papers.

## Before step 2, your own checks (optional)

- Paper B, Hoeffding (1951): Theorem 4 and condition (14) are cited on p. 560, which you confirmed.
- Paper A, Schneider: cited without a theorem number (Brunn–Minkowski is on pp. 71–72 of your edition).
- Paper A, Mino: the 2024 year you confirmed.

## Not needed for upload

- `arxiv_submission/` holds the earlier single-paper draft as a snapshot. Do not upload it.
- `Analysis/` holds the research and verification work behind both papers. Everything the papers rely on is copied into each paper's `anc/`.
