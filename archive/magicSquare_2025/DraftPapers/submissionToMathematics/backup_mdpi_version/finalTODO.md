# Final TODO List for Paper Submission to Experimental Mathematics
## Paper: "Geometric and Topological Analysis of Magic Squares"
## Target Journal: Experimental Mathematics (A K Peters / Taylor & Francis)
## Date: June 23, 2025

## Status Summary
Based on review of REVISION_SUMMARY.md, StatsRevision.md, FINAL_SUBMISSION_STATUS.md, and README.md:
- ✅ All statistical discrepancies have been corrected (880 unique squares)
- ✅ All missing figures have been created/located
- ✅ Validation script created and all stats verified
- ⚠️ Journal format conversion and submission items remain

## Critical Items Before Submission

### 1. Journal Format Conversion
- [ ] Convert from MDPI template to standard LaTeX article class (no two-column)
- [ ] Remove all MDPI-specific commands and metadata
- [ ] Keep standard packages:
  - `algorithm` and `algpseudocode` packages
  - `subcaption` package
  - `tikz` and `pgfplots` packages
- [ ] Test full compilation with article class
- [ ] Generate final PDF ensuring all formatting is correct

### 2. Citation Style Conversion
- [ ] Convert from numeric citations to author-year format
- [ ] Change citation commands from \cite{} to appropriate natbib commands
- [ ] Update bibliography style to author-year (e.g., [Smith 2021])
- [ ] Fix empty bibliography file (submission.bbl is empty)
- [ ] Copy references.bib from ../magic_squares/tex/bib/
- [ ] Run bibtex with appropriate style file
- [ ] Verify all citations display correctly in author-year format

### 3. Abstract and Content Adjustments
- [ ] Reduce abstract to ≤150 words (currently ~200 words)
- [ ] Ensure abstract is in English and self-contained
- [ ] Review paper for clarity and conciseness (no strict page limit)
- [ ] Include short code snippets where useful
- [ ] Add links to full code repository and data

### 4. Figure Format Conversion
- [ ] Convert all figures to high-quality EPS format
- [ ] Ensure no low-resolution images
- [ ] Update figure inclusion commands for EPS files
- [ ] Consider color figure costs (small fee per figure)

### 5. Author and Metadata Updates
- [ ] Update author information (currently lists "YourAI Assistant")
- [ ] Add author affiliations
- [ ] Add corresponding author email
- [ ] Remove all MDPI-specific metadata
- [ ] Remove MDPI-specific files (mdpi.cls, MDPI templates)

### 6. Submission Package Preparation
- [ ] Include all source files (.tex, .bib or .bbl, any macros)
- [ ] Ensure code_zip contains reproducible code
- [ ] Create links to online code/data repositories
- [ ] Prepare for online submission system OR print 2 copies if mailing
- [ ] No size restrictions but ensure reasonable file sizes

## Format Conversion Tasks

### From MDPI to Standard Article Class
- [ ] Create new submission_experimental_math.tex with article class
- [ ] Remove \documentclass[mathematics]{mdpi} and use \documentclass{article}
- [ ] Remove MDPI commands: \Title, \Author, \AuthorNames, etc.
- [ ] Convert to standard LaTeX title/author format
- [ ] Update section formatting to standard article style
- [ ] Remove MDPI-specific environments and commands

### Figure Conversion Script
- [ ] Create script to batch convert PNG/PDF figures to EPS
- [ ] Use ImageMagick or similar for high-quality conversion
- [ ] Verify all EPS files maintain quality
- [ ] Update all \includegraphics commands

### Bibliography Style Change
- [ ] Install and use natbib package
- [ ] Change bibliography style to author-year (e.g., plainnat)
- [ ] Update all \cite{} to \citep{} or \citet{} as appropriate
- [ ] Ensure format matches [Author Year] style

## Multiagent Review Process

### Phase 1: Technical Review (Agent 1 - Mathematical Rigor)
Focus: Mathematical correctness, proofs, and theoretical foundations
- [ ] Review zero-covariance proof in vector field section
- [ ] Verify dimensionality claim (d = n² - 2n)
- [ ] Check all mathematical notation consistency
- [ ] Validate statistical tests and p-values
- [ ] Review algorithmic complexity claims
- [ ] Ensure all theorems/lemmas are properly stated and proven

### Phase 2: Data & Results Review (Agent 2 - Empirical Validation)
Focus: Data accuracy, reproducibility, statistical analysis
- [ ] Verify all results use 880 unique squares dataset
- [ ] Cross-check all reported statistics against source data
- [ ] Review figure captions for accuracy
- [ ] Validate EMD and manifold analysis results
- [ ] Check that all code citations point to correct repositories
- [ ] Ensure reproducibility instructions are complete

### Phase 3: Writing & Clarity Review (Agent 3 - Communication)
Focus: Readability, flow, audience appropriateness
- [ ] Abstract: Ensure ≤150 words, clear main contributions
- [ ] Introduction: Check motivation and background are accessible
- [ ] Methods: Ensure reproducible step-by-step descriptions
- [ ] Results: Verify logical flow and clear presentation
- [ ] Discussion: Check interpretations are supported by data
- [ ] Conclusion: Ensure key takeaways are highlighted
- [ ] Remove any jargon without explanation
- [ ] Ensure code snippets are clear and well-integrated

### Phase 4: Journal Requirements Review (Agent 4 - Experimental Mathematics Compliance)
Focus: Journal-specific formatting and requirements
- [ ] Verify standard LaTeX article class (no two-column)
- [ ] Check citation style (author-year in brackets, e.g., [Smith 2021])
- [ ] Ensure abstract is ≤150 words
- [ ] Verify all figures are high-quality EPS format
- [ ] Check that code snippets are appropriately included
- [ ] Ensure links to full code/data repositories are provided
- [ ] Review paper for clarity and conciseness (no strict page limit)

### Phase 5: Final Integration Review (Agent 5 - Holistic Assessment)
Focus: Overall coherence and impact
- [ ] Ensure title accurately reflects content
- [ ] Verify abstract matches paper content
- [ ] Check that all claims are supported
- [ ] Review broader applications paragraph
- [ ] Ensure limitations are acknowledged
- [ ] Verify future work suggestions are reasonable
- [ ] Check overall narrative flow

## Additional Quality Checks

### Code and Reproducibility
- [ ] Run validate_statistics.py one final time
- [ ] Test run_all.py to ensure all figures can be regenerated
- [ ] Verify environment.yml includes all dependencies
- [ ] Check that Jupyter notebooks (if any) run without errors

### Figures and Tables
- [ ] Convert all figures to high-quality EPS format
- [ ] Ensure all figures have descriptive captions
- [ ] Check figure numbering is sequential
- [ ] Verify all figures are referenced in text
- [ ] Ensure color schemes are colorblind-friendly
- [ ] Check that tables are properly formatted
- [ ] Consider costs for color figures (small fee per figure)

### Supplementary Materials
- [ ] Organize supplementary files logically
- [ ] Create README for supplementary materials
- [ ] Ensure interactive visualizations work
- [ ] Check file sizes are reasonable

## Final Submission Steps

1. [ ] Complete all items above
2. [ ] Run final spell check
3. [ ] Generate final PDF with standard article class
4. [ ] Prepare/update cover letter for Experimental Mathematics
5. [ ] Choose submission method:
   - [ ] Online: Use journal's online management system (preferred)
   - [ ] Mail: Prepare 2 printed copies if necessary
6. [ ] Include all source files (.tex, .bib/.bbl, macros, EPS figures)
7. [ ] Submit and expect acknowledgment within ~2 weeks
8. [ ] Note submission ID/tracking information

## Post-Submission
- [ ] Prepare for potential reviewer comments
- [ ] Plan for creating Paper 2 on vector field representations
- [ ] Consider preprint options (arXiv)
- [ ] Plan social media/blog post about the work

## Folder Structure Update
- [ ] Consider renaming submission folder from "submissionToMathematics" to "submissionToExperimentalMathematics"
- [ ] Update all internal paths and references accordingly
- [ ] Ensure all scripts reference correct paths

## Notes
- The paper appears to be in excellent shape with most technical work complete
- Main tasks involve format conversion from MDPI to standard article class
- Citation style must be changed from numeric to author-year
- Abstract needs to be reduced from ~200 to ≤150 words
- All figures need conversion to EPS format
- No page charges expected (except small fee for color figures if used)
- The multiagent review process should catch any remaining issues
- Consider setting aside 3-4 days for format conversion and review process 