"""Tests for analyze module."""
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from titanic_analysis.analyze import TitanicAnalyzer
from titanic_analysis.config import Config


class TestTitanicAnalyzer:
    """Tests for TitanicAnalyzer class."""

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
  numerical_columns: ["age", "fare", "pclass"]
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
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
output:
  results_dir: "outputs"
  save_data: true
  save_figures: true
""")
            config_path = f.name

        config = Config(config_path)
        yield config
        Path(config_path).unlink()

    def test_analyzer_init(self, config):
        """Test analyzer initialization."""
        analyzer = TitanicAnalyzer(config_path=config.config_path)
        assert analyzer.data_loader is not None
        assert analyzer.visualizer is not None

    def test_run_analysis(self, config):
        """Test full analysis pipeline."""
        analyzer = TitanicAnalyzer(config_path=config.config_path)
        results = analyzer.run_analysis()

        assert "statistics" in results
        assert "plots" in results
        assert "data_shape" in results
        assert "columns" in results

        stats = results["statistics"]
        assert "total_passengers" in stats
        assert "survival_rate" in stats
        assert stats["total_passengers"] > 0
        assert 0 <= stats["survival_rate"] <= 1

    def test_compute_statistics(self, config):
        """Test statistics computation."""
        analyzer = TitanicAnalyzer(config_path=config.config_path)
        data = analyzer.data_loader.load()
        processed = analyzer.data_loader.preprocess(data)
        stats = analyzer._compute_statistics(processed)

        assert "total_passengers" in stats
        assert "survival_rate" in stats
        assert "missing_values" in stats
        assert "categorical_summary" in stats
        assert "numerical_summary" in stats

    def test_save_data(self, config, tmp_path):
        """Test data saving."""
        analyzer = TitanicAnalyzer(config_path=config.config_path)
        data = analyzer.data_loader.load()
        processed = analyzer.data_loader.preprocess(data)

        # Override output dir to temp
        analyzer.output_config["results_dir"] = str(tmp_path)
        analyzer._save_data(processed)

        saved_file = tmp_path / "titanic_processed.csv"
        assert saved_file.exists()

        # Verify saved data
        saved_data = pd.read_csv(saved_file)
        assert len(saved_data) == len(processed)
