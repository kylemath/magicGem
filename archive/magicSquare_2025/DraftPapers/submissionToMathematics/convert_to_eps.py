#!/usr/bin/env python3
"""
Convert PNG and PDF figures to high-quality EPS format for Experimental Mathematics submission.
Uses ImageMagick (convert command) for high-quality conversion.
"""

import os
import subprocess
from pathlib import Path
import argparse
import sys

def convert_to_eps(input_file, output_dir=None):
    """Convert a single image file to EPS format."""
    input_path = Path(input_file)
    
    if output_dir:
        output_path = Path(output_dir) / input_path.with_suffix('.eps').name
    else:
        output_path = input_path.with_suffix('.eps')
    
    # Skip if already exists
    if output_path.exists():
        print(f"  Skipping {input_path.name} (EPS already exists)")
        return True
    
    # Use ImageMagick convert command with high quality settings
    cmd = [
        'convert',
        str(input_path),
        '-density', '300',  # High resolution
        '-quality', '100',  # Maximum quality
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  Converted: {input_path.name} -> {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR converting {input_path.name}: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("ERROR: ImageMagick 'convert' command not found.")
        print("Please install ImageMagick: brew install imagemagick")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert figures to EPS format')
    parser.add_argument('--input-dir', default='figures', help='Input directory')
    parser.add_argument('--output-dir', help='Output directory (default: same as input)')
    parser.add_argument('--dry-run', action='store_true', help='List files without converting')
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"ERROR: Input directory '{input_dir}' does not exist")
        sys.exit(1)
    
    # Find all PNG and PDF files
    png_files = list(input_dir.glob('*.png'))
    pdf_files = list(input_dir.glob('*.pdf'))
    all_files = png_files + pdf_files
    
    if not all_files:
        print(f"No PNG or PDF files found in '{input_dir}'")
        return
    
    print(f"Found {len(png_files)} PNG and {len(pdf_files)} PDF files in '{input_dir}'")
    
    if args.dry_run:
        print("\nFiles to convert:")
        for f in sorted(all_files):
            print(f"  {f.name}")
        return
    
    # Create output directory if specified
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)
    else:
        output_dir = None
    
    # Convert all files
    print("\nConverting files to EPS format...")
    success_count = 0
    for file in sorted(all_files):
        if convert_to_eps(file, output_dir):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{len(all_files)} files converted successfully")
    
    # Update submission_experimental_math.tex if all conversions successful
    if success_count == len(all_files):
        print("\nAll conversions successful!")
        print("Remember to update \\includegraphics commands to use .eps extensions")
    else:
        print("\nSome conversions failed. Please check the errors above.")

if __name__ == '__main__':
    main() 