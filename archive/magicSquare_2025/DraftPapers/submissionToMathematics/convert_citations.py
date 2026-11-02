#!/usr/bin/env python3
"""
Convert citation commands from numeric (\cite{}) to author-year format.
Uses \citep{} for parenthetical citations and \citet{} for textual citations.
"""

import re
import os
from pathlib import Path
import argparse
import shutil

def convert_citations(text):
    """Convert \cite{} commands to natbib format."""
    
    # Pattern 1: "by \cite{...}" or "from \cite{...}" -> use \citet{}
    text = re.sub(r'\b(by|from|of)\s+\\cite\{', r'\1 \\citet{', text)
    
    # Pattern 2: Author names followed by \cite{} -> use \citep{}
    # e.g., "Euler \cite{euler1782}" -> "Euler \citep{euler1782}"
    text = re.sub(r'([A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?)\s+\\cite\{', r'\1 \\citep{', text)
    
    # Pattern 3: \cite{} at start of sentence -> use \citet{}
    text = re.sub(r'^\s*\\cite\{', r'\\citet{', text, flags=re.MULTILINE)
    text = re.sub(r'\.\s+\\cite\{', r'. \\citet{', text)
    
    # Pattern 4: All remaining \cite{} -> use \citep{}
    text = re.sub(r'\\cite\{', r'\\citep{', text)
    
    return text

def process_file(filepath, backup=True):
    """Process a single LaTeX file."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"ERROR: File '{filepath}' not found")
        return False
    
    # Read the file
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has citations
    if '\\cite{' not in content:
        print(f"  No citations found in {path.name}")
        return True
    
    # Create backup if requested
    if backup:
        backup_path = path.with_suffix('.tex.bak')
        shutil.copy2(path, backup_path)
        print(f"  Created backup: {backup_path.name}")
    
    # Convert citations
    new_content = convert_citations(content)
    
    # Count changes
    cite_count = content.count('\\cite{')
    citep_count = new_content.count('\\citep{')
    citet_count = new_content.count('\\citet{')
    
    # Write the modified content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Converted {path.name}: {cite_count} \\cite -> {citep_count} \\citep + {citet_count} \\citet")
    return True

def main():
    parser = argparse.ArgumentParser(description='Convert citations to author-year format')
    parser.add_argument('files', nargs='*', help='Files to process (default: all .tex in sections/)')
    parser.add_argument('--no-backup', action='store_true', help='Do not create backup files')
    args = parser.parse_args()
    
    # Get files to process
    if args.files:
        files = [Path(f) for f in args.files]
    else:
        # Process all .tex files in sections/
        sections_dir = Path('sections')
        if sections_dir.exists():
            files = list(sections_dir.glob('*.tex'))
        else:
            print("ERROR: No files specified and 'sections' directory not found")
            return
    
    if not files:
        print("No files to process")
        return
    
    print(f"Converting citations in {len(files)} files...")
    success_count = 0
    
    for file in sorted(files):
        if process_file(file, backup=not args.no_backup):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{len(files)} files processed successfully")
    
    # Also update the main file
    main_file = Path('submission_experimental_math.tex')
    if main_file.exists() and '\\cite{' in main_file.read_text():
        print(f"\nProcessing main file: {main_file.name}")
        process_file(main_file, backup=not args.no_backup)

if __name__ == '__main__':
    main() 