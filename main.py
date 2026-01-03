import argparse

from config import BOUTS_FILENAME, FENCER, TOUCHES_FILENAME
from src.analysis.action_correlation import run_no_priority_correlation
from src.analysis.action_predictor import FencingActionPredictor
from src.analysis.metrics import calculate_metrics
from src.analysis.metrics_analysis import analyze_fencer
from src.data.csv_fencer_action_provider import (
    CsvFencerActionProvider,
    CsvOrderedFencerActionProvider,
)
from src.domain.models import DataSources


def main():
    parser = argparse.ArgumentParser(description="Fencing Analysis Tool")
    parser.add_argument(
        "--analysis-type",
        choices=["metrics", "correlation", "predictor"],
        default="metrics",
        help="The type of analysis to run.",
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Date for metrics analysis",
    )
    parser.add_argument(
        "--bout-type",
        type=str,
        help="Bout type for metrics analysis",
    )
    args = parser.parse_args()

    sources = DataSources(touches_file=TOUCHES_FILENAME, bouts_file=BOUTS_FILENAME)

    if args.analysis_type == "metrics":
        provider = CsvFencerActionProvider(
            FENCER, sources, date=args.date, bout_type=args.bout_type
        )
        metrics = calculate_metrics(provider)
        print("------- Analysis --------")
        for metric in metrics:
            print(metric)
        print()
    elif args.analysis_type == "correlation":
        run_no_priority_correlation(data[0], FENCER)
    elif args.analysis_type == "predictor":
        provider = CsvOrderedFencerActionProvider(FENCER, data[0])
        predictor = FencingActionPredictor(provider)
        predictor.show_probabilities()


if __name__ == "__main__":
    main()
