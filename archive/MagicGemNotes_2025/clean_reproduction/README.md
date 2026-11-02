# Magic Squares: From Discrete Constraints to Continuous Geometry

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](paper/main.pdf)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **A Comprehensive Geometric Analysis of 4×4 Magic Squares**
>
> Kyle Elliott Mathewson  
> Department of Psychology, University of Alberta

## 🎯 Key Discovery: The Zero-Covariance Theorem

Magic squares are uniquely characterized by **four vanishing spatial-value covariances**. This provides a continuous geometric formulation of the discrete combinatorial constraints.

![Covariance Distribution](paper/figures/covariance_distribution.png)

**The plot above shows the smoking gun**: Among 300,000+ test arrangements (100k random, 100k one-swap, 100k two-swap perturbations), **only the 880 magic squares have zero covariance**. Even a single element swap destroys this property.

## 📊 What We Call "Magic Gems"

When we embed a magic square in R³ as (row, column, value) and compute the convex hull, we get a beautiful 3D polyhedron—a "Magic Gem."

![Hero Figure](paper/figures/hero_figure.png)

The transformation reveals:
- **16 points** from the 4×4 grid
- **12-14 hull vertices** (most common configurations)
- **Zero-covariance** in all spatial-value correlations
- **Perfect balance** when viewed as a physical system

## 🔬 Testing the Zero-Covariance Characterization

We rigorously tested whether the zero-covariance property is unique to magic squares:

| Arrangement Type | n | Mean (SD) | Minimum | Interpretation |
|-----------------|---|-----------|---------|----------------|
| **Magic Squares** | 880 | **0.000 (0.000)** | **0.000** | Theorem confirmed |
| One-Swap | 100,000 | 2.38 (1.12) | 0.20 | Clear gap |
| Semi-Magic | 10,000 | 0.85 (0.67) | 0.00 | Only magic at zero |
| Random | 100,000 | 5.55 (2.04) | 0.24 | Far from zero |

> **Key Finding**: Even a single element swap destroys the zero-covariance property. The minimum covariance sum among 100,000 one-swap perturbations was 0.20—never zero.

![Alternative Hypotheses](paper/figures/alternative_hypotheses_histograms.png)

## 🚀 Quick Start

### Setup
```bash
# Clone and enter directory
cd clean_reproduction

# Create virtual environment and install dependencies
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Full Reproduction
```bash
source venv/bin/activate
python run_reproduction.py
```

This will:
1. Load all 880 unique 4×4 magic squares
2. Run geometric analysis and generate all figures
3. Compile the LaTeX paper to PDF
4. Start the web dashboard (optional)

### Generate Specific Figures

```bash
# Hero figures (main visual results)
python src/create_hero_figures.py

# Alternative hypothesis testing
python src/alternative_hypotheses.py

# All visualizations
python -m src.visualize_comprehensive
```

## 📁 Project Structure

```
clean_reproduction/
├── README.md                 # This file
├── setup.sh                  # Environment setup script
├── requirements.txt          # Python dependencies
├── run_reproduction.py       # Main pipeline script
│
├── data/
│   └── all7040CategoriesData.csv  # Full dataset
│
├── src/                      # Analysis code
│   ├── core.py               # Core utilities
│   ├── features.py           # Feature extraction
│   ├── optimization.py       # Optimization algorithms
│   ├── validation.py         # Statistical validation
│   ├── benchmark.py          # Performance benchmarks
│   ├── create_hero_figures.py       # Publication figures
│   ├── alternative_hypotheses.py    # Hypothesis testing
│   ├── visualize.py          # General visualization
│   ├── visualize_comprehensive.py   # Full analysis plots
│   └── ...
│
├── paper/                    # LaTeX manuscript
│   ├── main.tex              # Main document
│   ├── main.pdf              # Compiled paper
│   ├── references.bib        # Bibliography
│   ├── sections/             # Modular sections
│   └── figures/              # Generated figures
│
├── paperReviewProcess/       # Editorial feedback
│   └── EditorFirstResponse.md
│
├── web/                      # Interactive dashboard
│   ├── index.html            # Main dashboard
│   └── visualization/        # 3D viewers
│
└── results/                  # Benchmark results
    └── benchmark/
```

## 📈 Key Results

### Geometric Invariants
- **Hull Volume**: 84.1 ± 7.1 cubic units (standard deviation)
- **Angular Uniformity**: 0.569 ± 0.000
- **21 Distinct Configurations** based on (vertices, face-points, interior)

### Algorithmic Performance (n=4 only)
- **73× speedup** over optimized backtracking (12.4ms vs 901.7ms)
- **99% success rate** with gradient-based optimization
- **95% CI**: [10.8ms, 14.2ms] for gradient method

> ⚠️ **Scope Note**: All empirical results are validated for n=4 only. Extension to larger n remains an open problem.

### Point Cloud Structure
- All 880 squares form a **single connected component**
- **Nearest-neighbor EMD**: 0.021 ± 0.011 (standard deviation)
- Uses "manifold" terminology informally for the embedded point cloud structure

## 🌐 Interactive Visualization

Start the web server:
```bash
cd web
python3 -m http.server 8000
```

Open http://localhost:8000 to explore:
- **Geometric Explorer**: Interactive 3D convex hulls
- **Manifold Navigator**: t-SNE visualization of all 880 squares
- **Research Overview**: Paper abstract and key findings

## 📚 Citation

```bibtex
@article{mathewson2025magic,
  title={From Discrete Constraints to Continuous Geometry: 
         A Comprehensive Analysis of Magic Squares Through 
         Covariance, Topology, and Optimization},
  author={Mathewson, Kyle Elliott},
  journal={Experimental Mathematics},
  year={2025},
  institution={University of Alberta}
}
```

## 🔗 Related Work

- Frenicle de Bessy (1693): Enumeration of 880 unique 4×4 squares
- Ollerenshaw & Brée (1998): Most-perfect pandiagonal squares
- Carlsson (2009): Persistent homology for point clouds
- Villani (2008): Optimal transport theory

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- University of Alberta for computational resources
- NSERC and CIFAR for research support
- The scientific Python community (NumPy, SciPy, Matplotlib)

---

**Questions?** Contact: kyle.mathewson@ualberta.ca
