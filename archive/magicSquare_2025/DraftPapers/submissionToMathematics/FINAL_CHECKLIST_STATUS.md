# Final Checklist Status for Experimental Mathematics Submission

## Completed Tasks ✅

### 1. Journal Format Conversion
- ✅ Converted from MDPI template to standard LaTeX article class
- ✅ Removed all MDPI-specific commands and metadata
- ✅ Kept standard packages (algorithm, algpseudocode, subcaption, tikz, pgfplots)
- ✅ Tested full compilation with article class
- ✅ Generated PDF with correct formatting

### 2. Citation Style Conversion
- ✅ Converted from numeric citations to author-year format
- ✅ Changed citation commands from \cite{} to \citep{} and \citet{}
- ✅ Updated bibliography style to author-year using plainnat
- ✅ Fixed empty bibliography file issue
- ✅ Copied references.bib from ../magic_squares/tex/bib/
- ✅ Ran bibtex successfully
- ✅ Verified all citations display correctly in author-year format

### 3. Abstract and Content Adjustments
- ✅ Reduced abstract to 147 words (< 150 word requirement)
- ✅ Ensured abstract is self-contained and in English
- ✅ Paper maintains clarity and includes code/algorithm references

### 4. Author and Metadata Updates
- ✅ Updated author information (removed "YourAI Assistant")
- ✅ Added proper author affiliation
- ✅ Added corresponding author email
- ✅ Removed all MDPI-specific metadata
- ✅ Removed MDPI-specific files (moved to backup_mdpi_version/)

### 5. File Organization
- ✅ Created backup_mdpi_version/ folder
- ✅ Moved all old MDPI files and .md documentation to backup
- ✅ Created new submission_experimental_math.tex
- ✅ Created shortened abstract file
- ✅ Created updated cover letter

## Remaining Tasks 📋

### 1. Figure Format Conversion
- ⏳ Convert all 42 PNG figures to high-quality EPS format
- ⏳ Update figure inclusion commands for EPS files
- ⏳ Consider color figure costs (small fee per figure)

### 2. Final Submission Package
- ⏳ Include all source files (.tex, .bib, .bbl, any macros)
- ⏳ Ensure code_zip contains reproducible code
- ⏳ Add GitHub repository link to cover letter
- ⏳ Prepare for online submission system

## Summary

We have successfully completed the major format conversion tasks:
- Document now uses standard article class (single column)
- Citations are in author-year format throughout
- Abstract meets the 150-word limit
- All MDPI-specific elements have been removed

The main remaining task is converting figures to EPS format, which can be done using the `convert_to_eps.py` script we created. After that, the paper will be ready for submission to Experimental Mathematics.

## Next Command to Run

```bash
python convert_to_eps.py
```

This will convert all 42 PNG figures to EPS format, after which the submission package will be complete. 