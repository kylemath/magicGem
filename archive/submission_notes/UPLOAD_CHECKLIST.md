# arXiv upload checklist: Magic Gems (A); Moments of Magic Squares (B) is on hold

Paper A no longer cites Paper B and uses none of its results (the one number it needed, the order-4 count in item (v) of A's changes list, is recounted in A's `anc/energy_zeros_count.py`). A can be uploaded on its own; B is not scheduled.

Branch `split-papers-a-b`. Both tarballs build from a clean directory with `pdflatex main; bibtex main; pdflatex main; pdflatex main` and match the committed PDFs.

| | Paper A | Paper B |
|---|---|---|
| Title | Magic Gems: Convex Hulls of Lifted Magic Squares | Moments of Magic Squares: Line-Sum Conditions, a Permutation Threshold, and Random Energies |
| arXiv action | **Replace** arXiv:2512.09170 (becomes v5) | On hold; would be a new submission |
| PDF | `paper_A_gems/paperA.pdf` (30 pp, 8 figures, 7 tables) | `paper_B_orthogonality/paperB.pdf` (27 pp, 3 figures, 4 tables) |
| Upload file | `paper_A_gems/paperA_arxiv.tar.gz` (801 KB) | `paper_B_orthogonality/paperB_arxiv.tar.gz` (418 KB) |
| Ancillary files | `anc/` at the top of the tarball (91 files) | `anc/` at the top of the tarball (78 files) |
| Metadata text | `paper_A_gems/submission_notes/arxiv_comments.md` | `paper_B_orthogonality/submission_notes/arxiv_metadata.md` |
| Abstract length | 1883 characters (limit 1920) | 1740 characters (limit 1920) |
| Primary category | math.CO | math.CO |
| Cross-lists | math.MG (optional) | math.PR; math.NT (optional) |
| MSC 2020 | 05B15, 52B05, 52B15, 52B20 | 05B20 (primary); 05A05, 11C08, 60C05, 60F05 |

## Order

0. **AI statement finalized & tarballs rebuilt:** The `[Author to confirm ...]` placeholders in `paper_*/sections/ai_statement.tex` and `paper_A_gems/submission/main.tex` have been replaced with `"The author has checked every proof in Sections ... and the appendices by hand."`, and both `paperA_arxiv.tar.gz` and `paperB_arxiv.tar.gz` have been rebuilt and verified. Paper A's item (v) withdraws v4's sampling claim; a rerun (anc/v4_sampling_recheck.py) backs the correction.
1. **Read both PDFs once yourself.** Check your name, affiliation and email on page 1. Both use `\today`, so arXiv stamps the date it compiles.
2. **Replace arXiv:2512.09170 with Paper A.**
   - Use "Replace", not "New submission", on 2512.09170.
   - Upload `paperA_arxiv.tar.gz` (rebuilt after step 0). arXiv picks up `anc/` as ancillary files automatically.
   - Use the comments and abstract from `arxiv_comments.md`. Change the title field to "Magic Gems: Convex Hulls of Lifted Magic Squares" (v1–v4 were "Magic Gems: A Polyhedral Framework for Magic Squares").
   - Ignore the "Candid list" section in that file; it is private notes.
3. **After it is announced:** nothing else is needed. Optionally, update the web app at kylemath.github.io/MagicGemWebpage to link the paper.
4. **Paper B, only if you decide to post it later:** a new submission from `paperB_arxiv.tar.gz` with the metadata in `arxiv_metadata.md` (CC BY 4.0 suggested). It already cites Paper A as arXiv:2512.09170, and A needs no change.

## Before uploading, your own checks (optional)

- Paper B, Hoeffding (1951): Theorem 4 and condition (14) are cited on p. 560, which you confirmed.
- Paper A, Schneider: cited without a theorem number (Brunn–Minkowski is on pp. 71–72 of your edition).
- Paper A, Mino: the 2024 year you confirmed.

## Not needed for upload

- The tarballs are built without macOS `._*` metadata files (build with `COPYFILE_DISABLE=1 tar ...` on a Mac, or arXiv receives a `._` twin of every file).
- `arxiv_submission/` holds the earlier single-paper draft as a snapshot. Do not upload it.
- `Analysis/` holds the research and verification work behind both papers. Everything the papers rely on is copied into each paper's `anc/`.
