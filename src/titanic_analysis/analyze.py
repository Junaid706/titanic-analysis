"""Main analysis module for Titanic Analysis."""
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any

from .config import get_config
from .logger import setup_logging
from .data import DataLoader
from .visualize import Visualizer


class TitanicAnalyzer:
    """Main analyzer class for Titanic dataset."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = get_config(config_path)
        self.logger = setup_logging("titanic_analysis.analyzer", config_path)
        self.data_loader = DataLoader(config_path)
        self.visualizer = Visualizer(config_path)
        self.output_config = self.config.get_section("output")

    def run_analysis(self) -> Dict[str, Any]:
        """Run complete analysis pipeline."""
        self.logger.info("Starting Titanic analysis...")

        # Load and preprocess data
        raw_data = self.data_loader.load()
        processed_data = self.data_loader.preprocess(raw_data)

        # Basic statistics
        stats = self._compute_statistics(processed_data)

        # Generate visualizations
        plot_paths = self.visualizer.generate_all_plots(processed_data)

        # Save processed data if configured
        if self.output_config.get("save_data", True):
            self._save_data(processed_data)

        results = {
            "statistics": stats,
            "plots": [str(p) for p in plot_paths],
            "data_shape": processed_data.shape,
            "columns": list(processed_data.columns),
        }

        self.logger.info("Analysis completed successfully")
        return results

    def _compute_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Compute basic statistics."""
        target = self.config.get("analysis.target_column", "survived")

        stats = {
            "total_passengers": len(data),
            "survival_rate": data[target].mean() if target in data.columns else None,
            "missing_values": data.isnull().sum().to_dict(),
            "categorical_summary": {},
            "numerical_summary": data.describe().to_dict(),
        }

        # Categorical summaries
        for col in self.config.get("analysis.categorical_columns", []):
            if col in data.columns:
                stats["categorical_summary"][col] = data[col].value_counts().to_dict()

        # Survival by category
        if target in data.columns:
            for col in self.config.get("analysis.categorical_columns", []):
                if col in data.columns:
                    stats[f"survival_by_{col}"] = data.groupby(col)[target].mean().to_dict()

        return stats

    def _save_data(self, data: pd.DataFrame) -> None:
        """Save processed data to CSV."""
        output_dir = Path(self.output_config.get("results_dir", "outputs"))
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / "titanic_processed.csv"
        data.to_csv(filepath, index=False)
        self.logger.info(f"Saved processed data to {filepath}")