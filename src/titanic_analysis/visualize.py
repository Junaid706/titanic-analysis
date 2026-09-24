"""Visualization module for Titanic Analysis."""

from pathlib import Path
from typing import Optional

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from .config import get_config  # noqa: E402
from .logger import setup_logging  # noqa: E402


class Visualizer:
    """Create and save visualizations for Titanic analysis."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = get_config(config_path)
        self.logger = setup_logging("titanic_analysis.viz", config_path)
        self.viz_config = self.config.get_section("visualization")
        self.analysis_config = self.config.get_section("analysis")
        self.output_dir = Path(self.viz_config.get("output_dir", "outputs"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._setup_style()

    def _setup_style(self) -> None:
        """Setup matplotlib and seaborn style."""
        sns.set_style(self.viz_config.get("style", "whitegrid"))
        sns.set_palette(self.viz_config.get("palette", "husl"))
        plt.rcParams["figure.figsize"] = self.viz_config.get("figure_size", [10, 6])
        plt.rcParams["figure.dpi"] = self.viz_config.get("dpi", 100)
        plt.rcParams["font.family"] = self.viz_config.get("font_family", "DejaVu Sans")

    def save_figure(self, name: str) -> Path:
        """Save current figure and return path."""
        if not self.viz_config.get("save_plots", True):
            return None

        filepath = self.output_dir / f"{name}.png"
        plt.tight_layout()
        plt.savefig(filepath, dpi=self.viz_config.get("dpi", 100), bbox_inches="tight")
        self.logger.info(f"Saved figure: {filepath}")
        plt.close()
        return filepath

    def plot_survival_by_class(self, data: pd.DataFrame) -> Path:
        """Plot survival count by passenger class."""
        plt.figure()
        sns.countplot(data=data, x="class", hue="survived")
        plt.title("Survival Count by Passenger Class")
        plt.xlabel("Passenger Class")
        plt.ylabel("Count")
        plt.legend(title="Survived", labels=["No", "Yes"])
        return self.save_figure("survival_by_class")

    def plot_age_distribution(self, data: pd.DataFrame) -> Path:
        """Plot age distribution with KDE."""
        plt.figure()
        sns.histplot(data=data, x="age", bins=30, kde=True)
        plt.title("Age Distribution of Passengers")
        plt.xlabel("Age")
        plt.ylabel("Count")
        return self.save_figure("age_distribution")

    def plot_survival_by_sex(self, data: pd.DataFrame) -> Path:
        """Plot survival rate by sex."""
        plt.figure()
        survival_rate = data.groupby("sex")["survived"].mean().reset_index()
        sns.barplot(data=survival_rate, x="sex", y="survived")
        plt.title("Survival Rate by Sex")
        plt.ylabel("Survival Rate")
        plt.ylim(0, 1)
        return self.save_figure("survival_by_sex")

    def plot_survival_by_embark_town(self, data: pd.DataFrame) -> Path:
        """Plot survival count by embarkation town."""
        plt.figure()
        sns.countplot(data=data, x="embark_town", hue="survived")
        plt.title("Survival Count by Embarkation Town")
        plt.xlabel("Embarkation Town")
        plt.ylabel("Count")
        plt.legend(title="Survived", labels=["No", "Yes"])
        return self.save_figure("survival_by_embark_town")

    def plot_fare_distribution(self, data: pd.DataFrame) -> Path:
        """Plot fare distribution by class."""
        plt.figure()
        sns.boxplot(data=data, x="class", y="fare")
        plt.title("Fare Distribution by Class")
        plt.ylabel("Fare")
        return self.save_figure("fare_by_class")

    def plot_correlation_heatmap(self, data: pd.DataFrame) -> Path:
        """Plot correlation heatmap for numerical features."""
        plt.figure(figsize=(10, 8))
        numerical = data.select_dtypes(include=[np.number])
        corr = numerical.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
        plt.title("Feature Correlation Heatmap")
        return self.save_figure("correlation_heatmap")

    def plot_survival_by_age_group(self, data: pd.DataFrame) -> Path:
        """Plot survival rate by age groups."""
        plt.figure()
        data = data.copy()
        age_bins = [0, 12, 18, 35, 50, 65, 100]
        age_labels = ["Child", "Teen", "Young Adult", "Adult", "Middle Age", "Senior"]
        data["age_group"] = pd.cut(data["age"], bins=age_bins, labels=age_labels)
        survival_rate = data.groupby("age_group", observed=False)["survived"].mean().reset_index()
        sns.barplot(data=survival_rate, x="age_group", y="survived")
        plt.title("Survival Rate by Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Survival Rate")
        plt.ylim(0, 1)
        plt.xticks(rotation=45)
        return self.save_figure("survival_by_age_group")

    def plot_family_size_survival(self, data: pd.DataFrame) -> Path:
        """Plot survival rate by family size."""
        plt.figure()
        data = data.copy()
        data["family_size"] = data["sibsp"] + data["parch"] + 1
        family_bins = [0, 1, 4, 11]
        family_labels = ["Solo", "Small (2-4)", "Large (5+)"]
        data["family_category"] = pd.cut(
            data["family_size"], bins=family_bins, labels=family_labels
        )
        survival_rate = (
            data.groupby("family_category", observed=False)["survived"].mean().reset_index()
        )
        sns.barplot(data=survival_rate, x="family_category", y="survived")
        plt.title("Survival Rate by Family Size")
        plt.xlabel("Family Size Category")
        plt.ylabel("Survival Rate")
        plt.ylim(0, 1)
        return self.save_figure("survival_by_family_size")

    def generate_all_plots(self, data: pd.DataFrame) -> list[Path]:
        """Generate all standard plots."""
        self.logger.info("Generating all visualizations...")
        paths = []

        plot_methods = [
            self.plot_survival_by_class,
            self.plot_age_distribution,
            self.plot_survival_by_sex,
            self.plot_survival_by_embark_town,
            self.plot_fare_distribution,
            self.plot_correlation_heatmap,
            self.plot_survival_by_age_group,
            self.plot_family_size_survival,
        ]

        for method in plot_methods:
            try:
                path = method(data)
                if path:
                    paths.append(path)
            except Exception as e:
                self.logger.error(f"Failed to generate {method.__name__}: {e}")

        self.logger.info(f"Generated {len(paths)} visualizations")
        return paths
