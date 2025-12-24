import pandas as pd

from action_predictor import FencingActionPredictor
from config import FENCER, FILENAME
from csv_fencer_action_provider import CsvOrderedFencerActionProvider
from process_df import add_touches_to_df


def main():
    main_df = pd.read_csv(FILENAME)
    main_df = add_touches_to_df(main_df)

    provider = CsvOrderedFencerActionProvider(FENCER, main_df)
    predictor = FencingActionPredictor(provider)
    predictor.show_probabilities()


if __name__ == "__main__":
    main()
