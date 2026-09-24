"""Tests for data module."""
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from titanic_analysis.config import Config
from titanic_analysis.data import DataLoader


class TestDataLoader:
    """Tests for DataLoader class."""

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
  categorical_columns: ["class", "sex"]
  numerical_columns: ["age", "fare"]
visualization:
  output_dir: "outputs"
logging:
  level: "INFO"
output:
  results_dir: "outputs"
""")
            config_path = f.name

        config = Config(config_path)
        yield config
        Path(config_path).unlink()

    def test_load_seaborn(self, config):
        """Test loading from seaborn."""
        loader = DataLoader(config_path=config.config_path)
        data = loader.load()

        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert "survived" in data.columns
        assert "class" in data.columns
        assert "age" in data.columns

    def test_preprocess_fills_missing(self, config):
        """Test preprocessing fills missing values."""
        loader = DataLoader(config_path=config.config_path)
        data = loader.load()
        processed = loader.preprocess(data)

        # Age should have no missing values after preprocessing
        assert processed["age"].isnull().sum() == 0

    def test_get_feature_target(self, config):
        """Test feature/target split."""
        loader = DataLoader(config_path=config.config_path)
        X, y = loader.get_feature_target()

        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert "survived" not in X.columns
        assert len(X) == len(y)
