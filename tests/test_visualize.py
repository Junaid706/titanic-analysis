"""Tests for visualization module."""

import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from titanic_analysis.config import Config
from titanic_analysis.visualize import Visualizer


class TestVisualizer:
    """Tests for Visualizer class."""

    @pytest.fixture
    def config(self):
        """Create test config."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("""
dataset:
  name: "titanic"
  source: "seaborn"
analysis:
  target_column: "survived"
  categorical_columns: ["class", "sex", "embark_town"]
  numerical_columns: ["age", "fare"]
visualization:
  style: "whitegrid"
  palette: "husl"
  figure_size: [10, 6]
  dpi: 100
  save_plots: true
  output_dir: "outputs"
  font_family: "DejaVu Sans"
logging:
  level: "INFO"
output:
  results_dir: "outputs"
""")
            config_path = f.name

        config = Config(config_path)
        yield config
        Path(config_path).unlink()

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        n = 100
        return pd.DataFrame(
            {
                "survived": np.random.randint(0, 2, n),
                "class": np.random.choice(["First", "Second", "Third"], n),
                "sex": np.random.choice(["male", "female"], n),
                "age": np.random.normal(30, 15, n).clip(0, 80),
                "fare": np.random.exponential(30, n).clip(0, 500),
                "embark_town": np.random.choice(["Southampton", "Cherbourg", "Queenstown"], n),
                "sibsp": np.random.poisson(0.5, n),
                "parch": np.random.poisson(0.3, n),
                "deck": np.random.choice(["A", "B", "C", "D", "E", "Unknown"], n),
                "alone": np.random.choice([True, False], n),
                "who": np.random.choice(["man", "woman", "child"], n),
            }
        )

    def test_visualizer_init(self, config):
        """Test visualizer initialization."""
        viz = Visualizer(config_path=config.config_path)
        assert viz.output_dir.exists()
        assert viz.viz_config is not None

    def test_plot_survival_by_class(self, config, sample_data):
        """Test survival by class plot."""
        viz = Visualizer(config_path=config.config_path)
        path = viz.plot_survival_by_class(sample_data)
        assert path is not None
        assert path.exists()

    def test_plot_age_distribution(self, config, sample_data):
        """Test age distribution plot."""
        viz = Visualizer(config_path=config.config_path)
        path = viz.plot_age_distribution(sample_data)
        assert path is not None
        assert path.exists()

    def test_plot_survival_by_sex(self, config, sample_data):
        """Test survival by sex plot."""
        viz = Visualizer(config_path=config.config_path)
        path = viz.plot_survival_by_sex(sample_data)
        assert path is not None
        assert path.exists()

    def test_generate_all_plots(self, config, sample_data):
        """Test generating all plots."""
        viz = Visualizer(config_path=config.config_path)
        paths = viz.generate_all_plots(sample_data)
        assert len(paths) > 0
        for path in paths:
            assert path.exists()
