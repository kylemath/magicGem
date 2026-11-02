#!/usr/bin/env python3
"""
Full Magic Squares Analysis Pipeline

This script runs the complete analysis pipeline:
1. Generate/load magic squares
2. Run geometric analysis
3. Run manifold analysis
4. Run EMD analysis
5. Generate visualizations
6. Generate LaTeX report
7. Compile PDF
"""

import os
import sys
import subprocess
import numpy as np
import shutil
from datetime import datetime
import logging
from pathlib import Path
import traceback
import yaml
import argparse

from magic_squares.src.generation.gen import generate_magic_squares
from magic_squares.src.analysis.analyze import run_analysis_pipeline
from magic_squares.src.analysis.report_generator import generate_report

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Magic Squares Analysis Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="magic_squares/config/pipeline_config.yaml",
        help="Path to pipeline configuration file"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()

def load_config(config_path):
    """Load pipeline configuration from YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

def setup_logging(run_dir, debug=False):
    """Set up logging configuration."""
    log_file = os.path.join(run_dir, "logs", "pipeline.log")
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def ensure_directory(directory):
    """Create directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    logging.debug(f"Ensured directory exists: {directory}")

def load_or_generate_squares(config):
    """Load existing squares or generate new ones if needed."""
    data_dir = Path("magic_squares/data")
    ensure_directory(data_dir)
    
    n_squares = config['squares']['n_squares']
    order = config['squares']['order']
    
    # Set random seed if specified
    if 'random_seed' in config['squares']:
        np.random.seed(config['squares']['random_seed'])
    
    # Check for existing squares
    square_files = list(data_dir.glob("magic_squares_*.npy"))
    if square_files:
        latest_file = max(square_files, key=lambda x: x.stat().st_mtime)
        logging.info(f"Loading existing squares from {latest_file}")
        squares = np.load(latest_file)
        
        if len(squares) >= n_squares:
            return squares[:n_squares]
        else:
            logging.info(f"Only found {len(squares)} squares, generating {n_squares - len(squares)} more")
            additional_squares = generate_magic_squares(n_squares - len(squares), order)
            squares = np.concatenate([squares, additional_squares])
    else:
        logging.info(f"No existing squares found, generating {n_squares} new squares")
        squares = generate_magic_squares(n_squares, order)
    
    # Save the squares
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = data_dir / f"magic_squares_{timestamp}.npy"
    np.save(save_path, squares)
    logging.info(f"Saved {len(squares)} squares to {save_path}")
    
    return squares

def validate_results(analysis_results, config):
    """Validate analysis results for completeness."""
    required_keys = []
    
    if config['analysis']['geometric']['enabled']:
        required_keys.append('geometric_analysis')
    if config['analysis']['manifold']['enabled']:
        required_keys.append('manifold_analysis')
    if config['analysis']['emd']['enabled']:
        required_keys.append('emd_analysis')
    
    required_keys.append('visualizations')
    
    missing_keys = [key for key in required_keys if key not in analysis_results]
    if missing_keys:
        logging.warning(f"Missing analysis results for: {', '.join(missing_keys)}")
        return False
    return True

def compile_latex(tex_file):
    """Compile LaTeX file to PDF."""
    tex_dir = os.path.dirname(tex_file)
    tex_filename = os.path.basename(tex_file)
    
    # Run pdflatex twice to resolve references
    for i in range(2):
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_filename],
                cwd=tex_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logging.error("LaTeX compilation failed:")
                logging.error(result.stderr)
                return False
                
        except Exception as e:
            logging.error(f"Error during LaTeX compilation: {str(e)}")
            return False
    
    pdf_file = tex_file.replace(".tex", ".pdf")
    if os.path.exists(pdf_file):
        logging.info(f"Successfully compiled PDF: {pdf_file}")
        return True
    else:
        logging.error("PDF compilation failed")
        return False

def setup_run_directory(config):
    """Create a new timestamped run directory with required subdirectories."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(config['output']['base_dir']) / timestamp
    
    # Create run directory and subdirectories
    for subdir in config['output']['subdirs']:
        ensure_directory(run_dir / subdir)
    
    return run_dir

def copy_template_files(run_dir, config):
    """Copy necessary template files to run directory."""
    template_dir = Path(config['report']['template_dir'])
    if template_dir.exists():
        for template in template_dir.glob("*.tex"):
            shutil.copy2(template, run_dir / template.name)
            logging.info(f"Copied template: {template.name}")

def compress_results(run_dir, config):
    """Compress results directory if configured."""
    if config['output'].get('compress_results', False):
        archive_name = f"{run_dir.name}_results.tar.gz"
        logging.info(f"Compressing results to {archive_name}")
        shutil.make_archive(
            str(run_dir / "results"),
            'gztar',
            str(run_dir / "results")
        )

def main():
    args = parse_args()
    config = load_config(args.config)
    
    try:
        # Create run directory and set up logging
        run_dir = setup_run_directory(config)
        logger = setup_logging(run_dir, args.debug)
        
        logger.info("=" * 80)
        logger.info("MAGIC SQUARES ANALYSIS PIPELINE")
        logger.info("=" * 80)
        
        # Step 1: Load or generate squares
        logger.info("\nStep 1: Loading/Generating Magic Squares")
        logger.info("-" * 40)
        squares = load_or_generate_squares(config)
        
        # Step 2: Run analysis pipeline
        logger.info("\nStep 2: Running Analysis Pipeline")
        logger.info("-" * 40)
        analysis_results = run_analysis_pipeline(
            squares,
            plots_dir=str(run_dir / "plots"),
            results_dir=str(run_dir / "results"),
            config=config['analysis']
        )
        
        # Validate results
        if not validate_results(analysis_results, config):
            logger.warning("Some analysis results are missing. Report may be incomplete.")
        
        # Step 3: Copy templates and generate LaTeX report
        logger.info("\nStep 3: Generating LaTeX Report")
        logger.info("-" * 40)
        copy_template_files(run_dir, config)
        
        tex_file = run_dir / "report.tex"
        generate_report(
            analysis_results,
            output_file=str(tex_file),
            title=config['report']['title'],
            author=config['report']['author']
        )
        
        # Step 4: Compile PDF
        logger.info("\nStep 4: Compiling PDF")
        logger.info("-" * 40)
        success = compile_latex(str(tex_file))
        
        # Step 5: Compress results if configured
        if success and config['output'].get('compress_results', False):
            compress_results(run_dir, config)
        
        if success:
            logger.info("\nPipeline completed successfully!")
            pdf_path = tex_file.with_suffix(".pdf")
            logger.info(f"Final report available at: {pdf_path}")
            logger.info(f"All run outputs are in: {run_dir}")
        else:
            logger.error("\nPipeline completed with errors in PDF compilation.")
            logger.error("Please check the LaTeX logs for details.")
        
    except Exception as e:
        logger.error("Pipeline failed with error:")
        logger.error(traceback.format_exc())
        sys.exit(1)
    
    logger.info("\nDone!")

if __name__ == "__main__":
    main() 