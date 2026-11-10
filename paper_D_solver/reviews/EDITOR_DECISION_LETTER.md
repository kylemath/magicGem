# Official Editorial Decision Letter & Remediation Roadmap

**Journal:** *Physical Review X / SIAM Review / INFORMS Journal on Computing* (Joint Interdisciplinary Special Track)  
**Manuscript ID:** `PRX-SIAM-2026-D0880`  
**Title:** *Can Physical Forces Find a Magic Square? Spectral Energy Landscapes, Symplectic Plaquette Exchanges, and Fast Bilinear Relaxation up to Order $n = 100$*  
**Author:** Dr. Kyle E. Mathewson  
**Handling Editor:** Prof. Henrik Lindqvist-Karger, Senior Handling Editor  
**Editorial Decision:** **CONDITIONAL ACCEPTANCE — Focused Revision Required (4-Gate Verification Roadmap)**  
**Date:** November 9, 2026  

---

## 1. Executive Summary of Editorial Decision

Dear Dr. Mathewson,

Your manuscript, *"Can Physical Forces Find a Magic Square? Spectral Energy Landscapes, Symplectic Plaquette Exchanges, and Fast Bilinear Relaxation up to Order $n = 100$,"* has now been evaluated by four leading experts across the four pillars of your study:
- **Reviewer 1 (Prof. Alistair Vance-Loly):** Algebraic Combinatorics, Spectral Graph Theory & Magic Square Matrices ([`REVIEWER_1_ALGEBRAIC_COMBINATORICS.md`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/reviews/REVIEWER_1_ALGEBRAIC_COMBINATORICS.md))
- **Reviewer 2 (Prof. Elena Rostova-Wales):** Statistical Physics, Energy Landscapes & Frustrated Lattice Dynamics ([`REVIEWER_2_STATISTICAL_PHYSICS_LANDSCAPES.md`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/reviews/REVIEWER_2_STATISTICAL_PHYSICS_LANDSCAPES.md))
- **Reviewer 3 (Prof. Marcus Van Hentenryck-Stützle):** Combinatorial Optimization, Metaheuristics & Constraint-Based Local Search ([`REVIEWER_3_COMBINATORIAL_OPTIMIZATION_CBLS.md`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/reviews/REVIEWER_3_COMBINATORIAL_OPTIMIZATION_CBLS.md))
- **Reviewer 4 (Prof. Clara Tufte-Krakauer):** Scientific Visualization, Complexity Science & Reproducibility Forensics ([`REVIEWER_4_VISUALIZATION_AND_FORENSICS.md`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/reviews/REVIEWER_4_VISUALIZATION_AND_FORENSICS.md))

Following receipt of the four independent reports, I convened a live **Editorial Panel Consultation** ([`EDITORIAL_PANEL_TRANSCRIPT.md`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/reviews/EDITORIAL_PANEL_TRANSCRIPT.md)) to reconcile the referees' perspectives and establish a single, unified set of revision requirements.

### Consensus Evaluation
The panel is unanimous that this manuscript is an extraordinary cross-disciplinary achievement:
1. **All six formal mathematical results**—Proposition 2.1 (diagonal-to-Rook subspace absorption and integer collapse on $\mathbf{1}^\perp$), Lemma 3.1 (interior vs. toroidal $2\times 2$ quartet identity), Proposition 3.2 (Concentric Shell Quadrupole Identity $M_{xyz} = -8Q_{\mathrm{corner}} - 3Q_{\mathrm{edge}}$ explaining the $56 = 48 + 8$ octupole zeros), Lemma 4.1 (Kawasaki quadratic transposition difference formula), Theorem 4.2 (exhaustive $S_9 = 362{,}880$ frustration census and unique skew $3$-column $(2,2)$ escape), and Theorem 6.1 ($O(n^3)$ bilinear plaquette identity $G = 2XX^\top$, active-set bound, and consecutive-value relay filter)—have been independently audited and verified to be **100% mathematically sound**.
2. **All nine 300-DPI figures (`fig1`–`fig9`)** passed visual and forensic inspection with high praise for their clean, annotation-free data canvases, despined axes, consistent Okabe–Ito/ColorBrewer semantics, and fidelity to `anc/results_paper_d.json`.
3. **Every discrepancy identified across the four reviews** stems from three localized, easily remediable sources:
   - Late-stage **manuscript-to-JSON synchronization lag** where `anc/results_paper_d.json` and `anc/make_figures_d.py` were updated during recent scaling runs, leaving several stale numbers in LaTeX captions and tables (specifically Figure 2b's `#123`/`#599` text values, Table 5's $n=3$ formula value, Figure 6c's caption percentages, Table 8/Fig. 7b's millisecond runtimes, and Table 9's $n=25, 30$ rows and trial-count prose);
   - The omission of the executable **Section 6 solver implementations** (`Bilinear-Identity + Active-Set ME-ILS`, `Defective-Line CBLS`, `Simulated Annealing`, and the $n=3\dots 50$ scaling loop) from `anc/verify_paper_d.py` (which currently verifies Sections 2–5 from scratch and passively reloads Section 6 from `results_paper_d.json`); and
   - **Terminology, convex-geometry, and baseline-framing refinements** requested by Reviewers 1, 2, and 3 to make the paper bulletproof for readers across algebraic combinatorics, statistical physics, and operations research.

Because every required modification is deterministic, localized, and does not alter any mathematical theorem or empirical conclusion, I am pleased to grant **Conditional Acceptance subject to Focused Revision**. Once you complete the **4-Gate Remediation Roadmap** itemized below, the manuscript can be accepted immediately without a second round of external panel review.

---

## 2. Prioritized 4-Gate Remediation Roadmap

To streamline your revision, the panel has organized all required edits into four self-contained verification gates.

---

### GATE 1: Code Archive & Reproducibility Completeness (`anc/verify_paper_d.py`)
*Source: Reviewer 3 (M3.1), Reviewer 4 (M4.2, m4.8), Reviewer 1 (M1.5).*

1. ** `[R-1.1]` Embed Executable Section 6 Solvers and Theorem 6.1 Unit Test into [`anc/verify_paper_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/verify_paper_d.py) (lines 1618–1647):**
   - Include the self-contained Python/NumPy implementations of:
     - `Bilinear-Identity + Active-Set ME-ILS` (implementing Theorem 6.1's active-set filter $\mathcal{A}(S)$, consecutive-value $|Z_a-Z_b|\le 2$ intra-line filter, and the $(K\times (n+2))$ Level-3 BLAS matrix multiplication `G = 2 * (X @ X.T)`),
     - `Baseline All-Pairs ME-ILS`,
     - `Defective-Line-Restricted CBLS`, and
     - `Simulated Annealing (Metropolis)`.
   - Add an automated **Theorem 6.1 Exactness Unit Check** inside `run_section6_large_scale_competition()` that runs fast by default (under 2 seconds, e.g., at $n=6, 10$) to verify that:
     1. Zero improving $1$-swaps exist outside $\mathcal{A}(S)\times \{1,\dots,n^2\}$,
     2. The bilinear matrix `dH1[:, None] + dH1[None, :] + 2 * (X @ X.T)` matches brute-force 4-cell evaluation across all non-overlapping row/column pairs to machine precision ($0.0$ error), and
     3. The consecutive-value filter $|Z_a-Z_b|\in\{1,2\}$ achieves $0\%$ false negatives on $R_L=0$ zero-residual relay swaps.
   - Provide a CLI flag (e.g., `--recompute-section6` or `--run-large-scale`) that regenerates `scan_10_to_50`, `bilinear_scaling`, and `competition_46_48_100` from scratch, while defaulting to the fast unit test + JSON verification so `python3 anc/verify_paper_d.py` completes in $<15\text{ s}$.
2. ** `[R-1.2]` Fix Two Stale Code Comments & Docstring in [`anc/verify_paper_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/verify_paper_d.py) and [`anc/make_figures_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/make_figures_d.py):**
   - In [`anc/verify_paper_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/verify_paper_d.py) lines 558 and 597, change `# 232 spurious local minima of S_9` to `# 8 spurious local minima of S_9 (all in D_4 orbit at E_std = 2, H_line = 8)`.
   - In [`anc/verify_paper_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/verify_paper_d.py) line 5, change `"Spectral Line-Incidence Laplacian"` to `"Spectral Line-Incidence Gram Operator"`.
   - In [`anc/make_figures_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/make_figures_d.py) lines 1–16, update the module docstring from `"7 publication-quality figures"` to list all 9 figures (`fig1_spectral_operator` through `fig9_competition_46_48_100`).

---

### GATE 2: Exact Numerical Synchronization Across LaTeX Tables, Captions & Markdown
*Source: Reviewer 4 (M4.1, M4.2, m4.1, m4.9, m4.10), Reviewer 1 (M1.3, M1.4, m1.3), Reviewer 2 (M2.3, M2.4), Reviewer 3 (m3.1–m3.4).*

Every hardcoded number in `paper_D_solver/sections/*.tex` and `PAPER_D_READABLE_MANUSCRIPT.md` must match `anc/results_paper_d.json` and the rendered figures 100%:

1. ** `[R-2.1]` Figure 6(c) Caption — Synchronize Stale Ablation Percentages ([`sections/continuous_vs_discrete.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/continuous_vs_discrete.tex#L66-L81) & [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L303)):**
   - Replace the stale multi-budget percentages in the Figure 6(c) caption (`18.25%`, `41.5%`, `87.0%/22.0%`, `98.5%/64.0%`, `100.0%/91.0%`) with the exact single-restart synthesis rates plotted in Figure 6(c), listed in Table 7 (`tab:physical_analogs_ablation`), and stored in `results_paper_d.json`:
     - **Tier 1 (Pure 2-Swap Steepest Descent):** $20.0\%$ ($n=4$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 16.3$) and $1.0\%$ ($n=5$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 30.8$).
     - **Tier 2 (Simulated Annealing):** $32.5\%$ ($n=4$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 13.7$) and $0.0\%$ ($n=5$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 37.8$).
     - **Tier 3 (2-Swap + 3-Cycle Descent):** $29.0\%$ ($n=4$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 14.5$) and $1.0\%$ ($n=5$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 25.0$).
     - **Tier 4 (2-Swap + (2,2) Plaquette Descent):** $42.5\%$ ($n=4$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 9.4$) and $2.0\%$ ($n=5$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 17.6$).
     - **Tier 5 (Single-Start Funnel-Leashed Basin-Hopping, 50 kicks):** $58.0\%$ ($n=4$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 5.4$) and $6.0\%$ ($n=5$, $\langle\mathcal{H}_{\mathrm{line}}\rangle = 15.8$).
     - **Tier 6 (Multi-Start Multi-Exchange ILS):** $100.0\%$ ($n=4$, $1.80$ mean restarts) and $100.0\%$ ($n=5$, $8.03$ mean restarts).
2. ** `[R-2.2]` Table 9 (`tab:scan_milestone_orders`) & Section 6.1 Prose — Fix $n=25, 30$ Cross-Experiment Mix-Up and Trial Schedule ([`sections/large_scale_competition.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/large_scale_competition.tex#L5-L42) & [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L332-L355)):**
   - Synchronize Table 9 (`tab:scan_milestone_orders`) so that every Baseline column reports `scan_10_to_50` from `results_paper_d.json` (matching Figure 8a/8b) while the parenthetical Bilinear time reports `bilinear_scaling`:
     - **$n=10$:** Restarts `2.80`, Descents `178.0`, Time `0.098 s` (`97.9 ms`).
     - **$n=15$:** Restarts `2.20`, Descents `225.7`, Time `0.36 s` (`0.09 s` Bilinear).
     - **$n=20$:** Restarts `5.00`, Descents `585.8`, Time `2.65 s` (`0.22 s` Bilinear).
     - **$n=25$:** Restarts `3.80` (was `1.67`), Descents `510.6` (was `296.3`), Time `6.66 s` (`0.54 s` Bilinear; note: `1.67` restarts / `296.3` descents / `0.54 s` is the Bilinear run at $n=25$).
     - **$n=30$:** Restarts `1.00` (was `8.67`), Descents `237.7` (was `1,233.3`), Time `4.53 s` (`1.37 s` Bilinear; note: `8.67` restarts / `1,205.3` descents / `1.37 s` is the Bilinear run at $n=30$).
     - **$n=35$:** Restarts `9.33`, Descents `1,547.7`, Time `65.91 s` (was `65.90 s`).
     - **$n=40$:** Restarts `5.67`, Descents `1,158.0`, Time `83.90 s` (`3.55 s` Bilinear).
     - **$n=50$:** Restarts `16.33`, Descents `4,104.3`, Time `796.79 s` (`12.22 s` Bilinear).
   - In Section 6.1 prose (line 8), state the exact trial schedule in `results_paper_d.json`: $N=10$ trials for $n=10\dots 16$, $N=5$ trials for $n=17\dots 25$, and $N=3$ trials for $n=26\dots 50$ ($195$ total trials across $n=10\dots 50$, $100\%$ solved).
   - In Section 6.1 prose (line 13), update the examples of orders achieving $1.00$ mean restarts in `scan_10_to_50` to $n=27, 30, 33$ (since $n=16$ had $1.80$ and $n=21$ had $1.60$ in `scan_10_to_50`, whereas $n=27, 30, 33$ all achieved exactly $1.00$ mean restart).
3. ** `[R-2.3]` Table 8 (`tab:multi_order_settler`), Figure 7(b) Caption & Section 5.3 Prose — Synchronize $n=3\dots 10$ Runtimes ([`sections/continuous_vs_discrete.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/continuous_vs_discrete.tex#L88-L137) & [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L307-L326)):**
   - Synchronize Table 8 (`tab:multi_order_settler`), the Figure 7(b) caption, and Section 5.3 text to match the `multi_order_upgraded` values plotted in Figure 7(b) from `results_paper_d.json`:
     - $n=3$: `0.1 ms` (was `0.1 ms` in Table 8, `0.62 ms` in Fig. 7b caption);
     - $n=4$: `5.8 ms` (`5.82 ms` in JSON; was `4.9 ms` in Table 8);
     - $n=5$: `92.8 ms` (`92.76 ms` in JSON; was `77.6 ms` in Table 8);
     - $n=6$: `90.2 ms` (`90.21 ms` in JSON; was `80.1 ms` in Table 8);
     - $n=7$: `193.7 ms` (`193.65 ms` in JSON; was `169.3 ms` in Table 8);
     - $n=8$: `344.2 ms` (`344.25 ms` in JSON; was `295.4 ms` in Table 8);
     - $n=9$: `870.5 ms` (`870.50 ms` in JSON; was `758.2 ms` in Table 8);
     - $n=10$: `1,001.6 ms` (`1001.55 ms` in JSON; was `880.8 ms` in Table 8 and Fig. 7b caption).
   - Also fix the stray LaTeX `&` separator in the $n=10$ row of Table 8 in [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L320) (`90,719,820 & 178.0 |` $\to$ `90,719,820 | 178.0 |`), and add a brief parenthetical note on line 100 of `continuous_vs_discrete.tex` explaining why $\langle\mathcal{H}_{\mathrm{line}}\rangle_{\mathrm{rand}} = 31{,}080$ at $n=6$ (empirical 5,000-sample estimate vs. exact $2\|\mathbf{z}\|^2 = 31{,}104$, difference $0.077\%$).
4. ** `[R-2.4]` Table 5 (`tab:s9_s16_landscape`) & Section 4.2 — Fix $n=3$ Plaquette Count $54$ vs. $18$ ([`sections/swap_landscape.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/swap_landscape.tex#L63-L105) & [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L214-L237)):**
   - At $n=3$, $2\binom{3}{2}^3 = 2\times 27 = 54$ ordered intra-row/intra-column $(2,2)$ selections, which collapse to $2\binom{3}{2}\binom{\binom{3}{2}}{2} = 18$ **unique** intra-line double swaps on a $3\times 3$ board because choosing two rows and a $2$-element column pair on a $3$-column grid leaves only $3$ distinct pairings of swaps (all $3$-column skew relays!), whereas aligned $2\times 2$ rectangular plaquettes number $\binom{3}{2}^2 = 9$ ($18$ across row/col). Update Table 5 and line 63 of `swap_landscape.tex` to state `54 (18 unique)` at $n=3$ and explain this exact distinction clearly.
5. ** `[R-2.5]` Figure 2(b) Caption & Section 3.3 Prose — Synchronize Squares `#123` and `#599` Quartet Values ([`sections/frenicle_880_landscape.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/frenicle_880_landscape.tex#L88-L118) & [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L168-L176)):**
   - In `results_paper_d.json` (`per_square_metrics`), both `#123` (max $H_{\mathrm{win}} = 1.000000\text{ bits}$) and `#599` (min $H_{\mathrm{win}} = 0.942535\text{ bits}$) have $W_{2\times 2}^{\mathrm{int}} = 512$ and $W_{2\times 2}^{\mathrm{tor}} = 1{,}024$ (which is where `make_figures_d.py` plots their markers in Figure 2b!), whereas squares `#145` (Group V, $H_{\mathrm{win}}=0.9963$) and `#219` (Group VI, $H_{\mathrm{win}}=0.9557$) realize the extreme interior values $W_{2\times 2}^{\mathrm{int}} = 384$ and $W_{2\times 2}^{\mathrm{int}} = 2{,}816$. Update Section 3.3 and the Figure 2(b) caption so that `#123` and `#599` are reported with their exact JSON values $W_{2\times 2}^{\mathrm{int}} = 512$ ($W_{2\times 2}^{\mathrm{tor}} = 1{,}024$).

---

### GATE 3: Theoretical, Physical & Algorithmic Framing Refinements
*Source: Reviewer 1 (M1.1–M1.3, m1.1–m1.2), Reviewer 2 (M2.1–M2.2, M2.4), Reviewer 3 (M3.2–M3.4, m3.4).*

1. ** `[R-3.1]` Title & Plaquette Terminology — Replace "Symplectic" with "Conjugate" or "Kempe Plaquette Exchanges" (Reviewer 1, M1.3):**
   - Update the manuscript title in [`main.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/main.tex#L29) and [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L1) from *"Symplectic Plaquette Exchanges"* to **"Conjugate Plaquette Exchanges"** (or **"Kempe Plaquette Exchanges"**), and explicitly distinguish in Section 4.2 / Section 5.3 between rectangular $2\times 2$ plaquettes ($4$-cycles of $K_{n,n}$ spanning the $(n-1)^2$-dimensional Rook nullspace) and skew $3$-column/row Kempe relay double swaps.
2. ** `[R-3.2]` Spectral Operator Nomenclature & $\mathbf{1}^\perp$ Restriction Notation (Reviewer 1, M1.1–M1.2, m1.1–m1.2):**
   - In Section 2.1 ([`sections/spectral_formulation.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/spectral_formulation.tex#L25-L85)), write out the explicit identity $L_{\mathrm{rc}} = 2nI_{n^2} - \Delta_{\mathrm{Rook}}$ relating the signless incidence Gram operator $L_n = A_n^\top A_n$ to the combinatorial Rook Laplacian $\Delta_{\mathrm{Rook}}$, and replace the phrase "spectral line-incidence Laplacian" in Section 7 (`discussion.tex` line 6) with "spectral line-incidence Gram operator".
   - Immediately after Eq. (36) in Proposition 2.1, state explicitly that $\widetilde{L}_n \in \operatorname{End}(\mathbf{1}^\perp)$ is the restricted $(n^2-1)\times(n^2-1)$ operator on the zero-sum hyperplane $\mathbf{1}^\perp$ (and label column 4 of Table 2 as $\operatorname{tr}(\widetilde{L}_n|_{\mathbf{1}^\perp}) = 2(n^2-1)$).
   - In Section 3.1/3.2 ([`sections/frenicle_880_landscape.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/frenicle_880_landscape.tex)), add a one-sentence explanation for why Dudeney Groups II, III, and V have group-mean $\langle W_{2\times 2}^{\mathrm{int}}\rangle = \|\mathbf{z}\|^2 = 1{,}360$ (vanishing nearest-neighbor autocorrelation under their involutive pairings) and note the Cousin–Ollerenshaw row/column parity involution $\pi=(2,4,1,3)$ mapping Group IX to Group X while flipping the sign of $W_{2\times 2}^{\mathrm{int}} - 1{,}360$.
3. ** `[R-3.3]` Birkhoff Polytope Convexity & Bauer's Maximum Principle in Section 5.1 (Reviewer 2, M2.1):**
   - In Section 5.1 ([`sections/continuous_vs_discrete.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/continuous_vs_discrete.tex#L22-L42)), explain mathematically why continuous 2D bubbles "cheat" via border parking: because $L_n = A_n^\top A_n \succeq 0$ is positive semidefinite, $\mathcal{H}_{\mathrm{ind}}(W) = \mathbf{z}^\top W L_n W^\top \mathbf{z}$ is **convex** on the Birkhoff polytope $\mathcal{B}_{n^2}$, so by Bauer's Maximum Principle its minimum lies at the interior barycenter $W_{\mathrm{bary}} = \frac{1}{n^2}\mathbf{1}\mathbf{1}^\top$ ($\widetilde{\mathbf{z}}=\mathbf{0}$), whereas driving trajectories to the extreme permutation vertices $P \in S_{n^2}$ requires a **concave** quadratic-assignment penalty $\mathcal{H}_\gamma(P) = \operatorname{tr}(P^\top L_n P \mathbf{z}\mathbf{z}^\top) - \gamma \|P\|_F^2$ with $\gamma > \lambda_{\max}(\widetilde{L}_n) = n$.
4. ** `[R-3.4]` Canonical Metropolis Basin-Hopping vs. Deterministic Funnel Re-Anchoring Leash in Section 5.2 (Reviewer 2, M2.2):**
   - In Section 5.2 ([`sections/continuous_vs_discrete.tex`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/sections/continuous_vs_discrete.tex#L44-L65)), explicitly distinguish canonical Metropolis Basin-Hopping (Wales & Doye 1997) from Tier 5's deterministic hard-wall **Funnel Re-Anchoring Leash** ($\mathcal{H}_{\mathrm{line}} \le \mathcal{H}_{\min} + 24s_{\mathrm{fac}}(n)$) and Tier 6's multi-start ILS, explaining via the super-exponential configurational entropy gradient $\partial S_{\mathrm{conf}}/\partial \mathcal{H}_{\mathrm{line}} \gg 0$ why hard-wall re-anchoring prevents entropic escape from the ground-state funnel.
5. ** `[R-3.5]` Sublinear Restart Drift ($K=40$), Trajectory Divergence, Speedup Factorization & Fair CBLS Attribution in Section 6 (Reviewer 2, M2.4; Reviewer 3, M3.2–M3.4, m3.4):**
   - **Sublinear Restart Drift (Section 6.1):** Note transparently that while restarts are order-invariant to first order across $n \in [6, 50]$ (linear regression $p = 0.24$), the 5-order moving average shows a mild sublinear rise from $\sim 3.5$ restarts ($n \in [10,25]$) to $\sim 9.5$ restarts ($n \in [35,50]$) because the candidate list size $K=40$ is held constant rather than scaled linearly with $n$.
   - **Trajectory Divergence & Speedup Decomposition (Section 6.2/6.3):** Explain why `Baseline All-Pairs ME-ILS` and `Bilinear + Active-Set ME-ILS` follow distinct early descent trajectories on the same random seed (`[7, 24, 16]` vs. `[32, 9, 17]` restarts at $n=46$) due to the two-stage top-$2n$ active-set pivot waterfall and $K \le 800$ bilinear candidate cap (before certifying exact $2$-exchange local minima at the bottom of the funnel), and explicitly factor the $34.7\times\text{--}50.2\times$ wall-clock speedup into $\sim 18.1\times\text{--}18.8\times$ algorithmic candidate reduction times $\sim 1.9\times\text{--}2.3\times$ Level-3 BLAS (`GEMM`) hardware throughput.
   - **Fair CBLS Attribution (Section 6.3):** Distinguish the tested *Defective-Line-Restricted CBLS* heuristic (which restricts $(2,2)$ candidate generation to defective lines $R_L \ne 0$ and top-$25$ truncation) from classical *Adaptive Search* (Codognet & Diaz 2001; Van Hentenryck & Michel 2005), noting how Adaptive Search's variable-conflict selection across all partner cells aligns with Theorem 6.1(1) for $1$-swaps while $2$-swap zero-residual relays require initiating $p_1$ on an already balanced line ($R_{r_1}=0$).
   - **Complete Theorem 6.1 in Readable Markdown:** Add the non-overlapping support hypothesis ($\operatorname{supp}(p_1)\cap\operatorname{supp}(p_2)=\emptyset$) and the full proof of Theorem 6.1 to [`PAPER_D_READABLE_MANUSCRIPT.md`](file:///Users/kylemathewson/.gemini/antigravity/brain/aafbf823-ba8c-4876-bb41-39f48620c033/PAPER_D_READABLE_MANUSCRIPT.md#L358-L370) so it matches `large_scale_competition.tex`.

---

### GATE 4: Surgical Visual Layout Polish (`anc/make_figures_d.py`)
*Source: Reviewer 4 (M4.3, m4.2–m4.7, m4.11), Reviewer 1 (m1.3).*

Apply the following clean layout adjustments in [`anc/make_figures_d.py`](file:///Users/kylemathewson/Downloads/MagicGemPaperC/paper_D_solver/anc/make_figures_d.py) and regenerate all 9 PDF/PNG figures:
1. ** `[R-4.1]` Figure 4(a) & 4(b) (`fig4_s9_landscape_traps.png`):**
   - Move the low-energy inset slightly left and higher (`ax_ins = ax0.inset_axes([0.10, 0.43, 0.38, 0.30])` and `ax0.set_ylim(0, 39500)`) so its bottom-right border and tick labels do not touch the rising navy histogram bars at $\mathcal{H}_{\mathrm{line}} \in [280, 430]$.
   - Add a bold panel title `(b) 3-Stage Combination-Lock Escape Pathway` above the right subgrid `gs[0, 1]` to match Panel `(a)`.
2. ** `[R-4.2]` Figure 7(a) & 7(b) (`fig7_multi_order_dimensional_relief.png`):**
   - Update `ax0.set_xlabel("Grid order n (Maxwell-Calladine ratio \\eta_{MC})")` so the parenthetical x-tick values `n=3 (0.3)`–`n=10 (4.0)` are explicitly identified.
   - Increase `ax1_r.set_ylim(0, 1120)` so the top diamond marker at $n=10$ (`1001.55 ms`) is not clipped by the top axis boundary, and align Panel `(b)`'s title with the plotted curves.
3. ** `[R-4.3]` Minor Typography & Headroom Refinements (`fig1`, `fig2`, `fig3`, `fig5`, `fig6`, `fig9`):**
   - **Fig. 1(b):** Soften the diagonal guide lines to `alpha=0.45, lw=1.2`.
   - **Fig. 2(b):** Expand `ax1.set_ylim(0.936, 1.022)` so the upper-right legend has generous whitespace above the top scatter points.
   - **Fig. 3(a), Fig. 5(b), Fig. 9(a):** Replace `{,}` inside plain matplotlib math strings (`$31{,}104$`, `$65{,}536$`) with standard comma formatting (`31,104`, `65,536`) so matplotlib's mathtext parser does not add extra space after the comma.
   - **Fig. 5(a):** Replace ASCII `--` with a proper Unicode en-dash `–` in `"Median (IQR 20%–80%)"`.
   - **Fig. 6(b):** Add `ax1.set_ylabel("Grid row y")` to match Panel `(a)`.

---

We look forward to receiving your revised manuscript and updated verification suite. Congratulations once again on a landmark contribution to the mathematics and physics of combinatorial landscapes.

Sincerely,

**Prof. Henrik Lindqvist-Karger**  
Senior Handling Editor  
*Joint Editorial Board — Physical Review X / SIAM Review / INFORMS Journal on Computing*
