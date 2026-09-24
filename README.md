# 🚢 Titanic Analysis Project

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Tests](https://github.com/USERNAME/titanic-analysis/actions/workflows/test.yml/badge.svg)](https://github.com/USERNAME/titanic-analysis/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A professional, modular Python project for analyzing the Titanic dataset with advanced visualizations, CLI interface, and comprehensive testing.

---

## 📊 Results Preview

| Survival by Class | Age Distribution |
|:---:|:---:|
| ![Survival by Class](outputs/survival_by_class.png) | ![Age Distribution](outputs/age_distribution.png) |

| Survival by Sex | Correlation Heatmap |
|:---:|:---:|
| ![Survival by Sex](outputs/survival_by_sex.png) | ![Correlation Heatmap](outputs/correlation_heatmap.png) |

**Key Findings:**
- **Overall survival rate: 38.38%** (891 passengers)
- **1st class passengers** had ~63% survival vs **3rd class** ~24%
- **Women** survived at ~74% vs **men** ~19%
- **Children** had higher survival rates than adults

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏗️ **Modular Architecture** | Clean separation: config, data, visualization, analysis, CLI |
| ⚙️ **YAML Configuration** | All settings externalized — no code changes needed |
| 📈 **8 Publication-Quality Plots** | Saved as high-DPI PNG, non-interactive backend |
| 🖥️ **Rich CLI** | `argparse` with subcommands, help, verbose mode |
| 📝 **Structured Logging** | Console + file, configurable levels |
| 🧪 **12 Unit Tests** | Covering data, visualization, analysis modules |
| 🔧 **Extensible** | Easy to add new analyses/visualizations |

---

## 📁 Project Structure

```
titanic-analysis/
├── .github/workflows/       # GitHub Actions CI
├── config/
│   └── settings.yaml        # All configuration
├── src/
│   └── titanic_analysis/    # Main package
│       ├── __init__.py
│       ├── config.py        # Config loader
│       ├── logger.py        # Logging setup
│       ├── data.py          # Data loading & preprocessing
│       ├── visualize.py     # 8 visualization methods
│       ├── analyze.py       # Analysis pipeline
│       └── cli.py           # Command-line interface
├── tests/
│   ├── test_data.py
│   ├── test_visualize.py
│   └── test_analyze.py
├── outputs/                 # Generated plots + CSV (gitignored)
├── logs/                    # Execution logs (gitignored)
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation

```bash
# Clone & enter
git clone https://github.com/USERNAME/titanic-analysis.git
cd titanic-analysis

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\Activate.ps1       # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

### Run Analysis

```bash
# Full analysis (plots + stats + CSV)
python -m src.titanic_analysis.cli

# Options
python -m src.titanic_analysis.cli --data-only    # Statistics only
python -m src.titanic_analysis.cli --plots-only   # Generate plots only
python -m src.titanic_analysis.cli -v             # Verbose logging
python -m src.titanic_analysis.cli --help         # Show all options
```

### Outputs Generated

```
outputs/
├── survival_by_class.png
├── age_distribution.png
├── survival_by_sex.png
├── survival_by_embark_town.png
├── fare_by_class.png
├── correlation_heatmap.png
├── survival_by_age_group.png
├── survival_by_family_size.png
└── titanic_processed.csv    # Cleaned dataset

logs/
└── analysis.log
```

---

## ⚙️ Configuration

Edit `config/settings.yaml`:

```yaml
dataset:
  name: "titanic"
  source: "seaborn"          # or "local", "kaggle"

visualization:
  style: "whitegrid"
  palette: "husl"
  figure_size: [10, 6]
  dpi: 300                   # High-res for publications
  save_plots: true
  output_dir: "outputs"

analysis:
  target_column: "survived"
  categorical_columns: ["class", "sex", "embark_town", "deck", "alone"]
  numerical_columns: ["age", "fare", "pclass", "sibsp", "parch"]
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/titanic_analysis --cov-report=term-missing
```

**CI Pipeline:** Tests run automatically on every push/PR via GitHub Actions.

---

## 📦 Using as a Library

```python
from titanic_analysis import TitanicAnalyzer

analyzer = TitanicAnalyzer()
results = analyzer.run_analysis()

print(f"Survival rate: {results['statistics']['survival_rate']:.1%}")
print(f"Plots generated: {len(results['plots'])}")
```

---

## 🔧 Tech Stack

| Category | Tools |
|----------|-------|
| **Data** | pandas, numpy |
| **Visualization** | matplotlib, seaborn |
| **Config** | pyyaml |
| **Testing** | pytest, pytest-cov |
| **CI/CD** | GitHub Actions |

---

## 📄 License

MIT License — feel free to use, modify, distribute.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

⭐ **Star this repo if you find it useful!**