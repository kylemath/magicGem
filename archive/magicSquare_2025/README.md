# Magic Squares Analysis Pipeline

A comprehensive pipeline for analyzing the geometric and topological properties of magic squares.

## Overview

This project provides a complete analysis pipeline for studying magic squares, including:
- Geometric analysis of point distributions
- Manifold learning and dimensionality reduction
- Earth Mover's Distance (EMD) based comparisons
- Automated report generation with visualizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/magicSquare.git
cd magicSquare
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the pipeline with default settings:
```bash
python run_full_pipeline.py
```

Run with debug logging:
```bash
python run_full_pipeline.py --debug
```

Use a custom configuration file:
```bash
python run_full_pipeline.py --config path/to/config.yaml
```

### Configuration

The pipeline is configured using a YAML file (`magic_squares/config/pipeline_config.yaml`). Key configuration options include:

- Square generation settings
- Analysis parameters
- Visualization options
- Report customization
- Output directory structure

See the example configuration file for all available options.

### Output Structure

The pipeline creates a timestamped directory for each run under `magic_squares/runs/` with the following structure:

```
YYYYMMDD_HHMMSS/
├── plots/          # Generated visualizations
├── results/        # Analysis results
├── logs/          # Pipeline logs
├── report.tex      # Generated LaTeX report
└── report.pdf      # Compiled PDF report
```

## Pipeline Steps

1. **Square Generation/Loading**
   - Generate new magic squares or load existing ones
   - Configurable number and order of squares

2. **Geometric Analysis**
   - Point distribution patterns
   - Convex hull properties
   - Angular uniformity measures

3. **Manifold Analysis**
   - Dimension estimation
   - Local structure analysis
   - Curvature properties

4. **EMD Analysis**
   - Pairwise distance computations
   - Multi-scale analysis
   - Flow visualizations

5. **Report Generation**
   - LaTeX report with results and visualizations
   - Configurable sections and content
   - Automatic PDF compilation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 