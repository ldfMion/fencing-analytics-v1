import argparse
import pandas as pd

from action_correlation import run_no_priority_correlation
from action_predictor import FencingActionPredictor
from config import FENCER, FILENAME
from csv_fencer_action_provider import CsvOrderedFencerActionProvider
from data_loader import add_touches_to_df
from services import analyze_fencer


def main():
    parser = argparse.ArgumentParser(description="Fencing Analysis Tool")
    parser.add_argument(
        "--analysis-type",
        choices=["metrics", "correlation", "predictor"],
        default="metrics",
        help="The type of analysis to run.",
    )
    args = parser.parse_args()

    main_df = pd.read_csv(FILENAME)
    main_df = add_touches_to_df(main_df)

    if args.analysis_type == "metrics":
        analyze_fencer(main_df, FENCER)
    elif args.analysis_type == "correlation":
        run_no_priority_correlation(main_df, FENCER)
    elif args.analysis_type == "predictor":
        provider = CsvOrderedFencerActionProvider(FENCER, main_df)
        predictor = FencingActionPredictor(provider)
        predictor.show_probabilities()


if __name__ == "__main__":
    main()
