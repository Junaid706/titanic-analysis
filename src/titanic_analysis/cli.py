"""Command-line interface for Titanic Analysis."""
import argparse
import sys
from pathlib import Path

from .config import get_config
from .logger import setup_logging
from .analyze import TitanicAnalyzer


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Titanic Dataset Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m titanic_analysis.cli                    # Run full analysis
  python -m titanic_analysis.cli --config custom.yaml  # Use custom config
  python -m titanic_analysis.cli --plots-only       # Generate only plots
  python -m titanic_analysis.cli --data-only        # Show data statistics only
        """
    )
    parser.add_argument(
        "-c", "--config",
        type=str,
        help="Path to configuration YAML file"
    )
    parser.add_argument(
        "--plots-only",
        action="store_true",
        help="Generate only visualizations"
    )
    parser.add_argument(
        "--data-only",
        action="store_true",
        help="Show only data statistics"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Override output directory for plots and results"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Titanic Analysis 1.0.0"
    )
    return parser


def main(args: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Setup logging
    log_level = "DEBUG" if parsed_args.verbose else "INFO"
    logger = setup_logging("titanic_analysis.cli")
    logger.setLevel(log_level)

    try:
        # Load config
        config = get_config(parsed_args.config)

        # Override output dir if provided
        if parsed_args.output_dir:
            config._config.setdefault("visualization", {})["output_dir"] = parsed_args.output_dir
            config._config.setdefault("output", {})["results_dir"] = parsed_args.output_dir

        analyzer = TitanicAnalyzer(parsed_args.config)

        if parsed_args.data_only:
            # Load data and show stats only
            data = analyzer.data_loader.load()
            processed = analyzer.data_loader.preprocess(data)
            stats = analyzer._compute_statistics(processed)

            print(f"\nDataset Shape: {processed.shape}")
            print(f"Columns: {list(processed.columns)}")
            print(f"\nTotal Passengers: {stats['total_passengers']}")
            print(f"Survival Rate: {stats['survival_rate']:.2%}")
            print(f"\nMissing Values:")
            for col, count in stats['missing_values'].items():
                if count > 0:
                    print(f"  {col}: {count}")

            return 0

        if parsed_args.plots_only:
            # Generate plots only
            data = analyzer.data_loader.load()
            processed = analyzer.data_loader.preprocess(data)
            paths = analyzer.visualizer.generate_all_plots(processed)
            print(f"\nGenerated {len(paths)} plots in {analyzer.visualizer.output_dir}")
            return 0

        # Run full analysis
        results = analyzer.run_analysis()

        print("\n" + "=" * 50)
        print("TITANIC ANALYSIS RESULTS")
        print("=" * 50)
        print(f"Dataset Shape: {results['data_shape']}")
        print(f"Total Passengers: {results['statistics']['total_passengers']}")
        print(f"Overall Survival Rate: {results['statistics']['survival_rate']:.2%}")
        print(f"\nGenerated Plots: {len(results['plots'])}")
        for plot in results['plots']:
            print(f"  - {plot}")

        return 0

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=parsed_args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())