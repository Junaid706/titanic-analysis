"""Data loading and preprocessing for Titanic Analysis."""
from pathlib import Path
from typing import Optional

import pandas as pd
import seaborn as sns

from .config import get_config
from .logger import setup_logging


class DataLoader:
    """Load and preprocess Titanic dataset."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = get_config(config_path)
        self.logger = setup_logging("titanic_analysis.data", config_path)
        self.dataset_config = self.config.get_section("dataset")
        self._data: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        """Load dataset based on configuration."""
        source = self.dataset_config.get("source", "seaborn")
        name = self.dataset_config.get("name", "titanic")

        self.logger.info(f"Loading dataset: {name} from {source}")

        if source == "seaborn":
            self._data = sns.load_dataset(name)
        elif source == "local":
            local_path = self.dataset_config.get("local_path")
            if local_path and Path(local_path).exists():
                self._data = pd.read_csv(local_path)
            else:
                raise FileNotFoundError(f"Local dataset not found: {local_path}")
        else:
            raise ValueError(f"Unsupported data source: {source}")

        self.logger.info(f"Loaded {len(self._data)} rows, {len(self._data.columns)} columns")
        return self._data

    def get_data(self) -> pd.DataFrame:
        """Get loaded data, loading if necessary."""
        if self._data is None:
            return self.load()
        return self._data

    def preprocess(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Basic preprocessing of Titanic data."""
        data = df if df is not None else self.get_data()
        data = data.copy()

        # Fill missing age with median
        if "age" in data.columns:
            data["age"] = data["age"].fillna(data["age"].median())

        # Fill missing embarked with mode
        if "embarked" in data.columns:
            data["embarked"] = data["embarked"].fillna(data["embarked"].mode()[0])

        # Fill missing deck with "Unknown"
        if "deck" in data.columns:
            if data["deck"].dtype.name == "category":
                data["deck"] = data["deck"].cat.add_categories("Unknown")
            data["deck"] = data["deck"].fillna("Unknown")

        self.logger.info("Preprocessing completed")
        return data

    def get_feature_target(
        self, df: Optional[pd.DataFrame] = None
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Split features and target."""
        data = self.preprocess(df)
        target_col = self.config.get("analysis.target_column", "survived")

        X = data.drop(columns=[target_col], errors="ignore")
        y = data[target_col] if target_col in data.columns else None

        return X, y
