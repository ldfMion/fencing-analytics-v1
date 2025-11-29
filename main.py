from typing import cast

import pandas as pd

from csv_fencer_action_provider import CsvFencerActionProvider
from metrics import MetricsCalculator
from process_df import add_touches_to_df, get_bouts_from_df

FILENAME = "Elite Invitationals 2025 Analytics.csv"
FENCER = "Mion"


def main():
    main_df = pd.read_csv(FILENAME)
    main_df = add_touches_to_df(main_df)

    sources = {
        "overall": main_df,
        "Day 1": main_df[main_df["Date"] == "08/11/25"],
        "Day 2": main_df[main_df["Date"] == "09/11/25"],
        "4-4": main_df[(main_df["Left Score"] == 4) & (main_df["Right Score"] == 4)],
    }

    for name, df in sources.items():
        metrics = MetricsCalculator(CsvFencerActionProvider(FENCER, df))
        result = metrics.calculate()
        print(f"------- Analysis: {name} --------")
        for metric in result:
            print(metric)
        print()

    bouts = get_bouts_from_df(main_df)
    print("Analyzing bouts: ")
    for _, bout in bouts.iterrows():
        left = bout["Left Fencer"]
        right = bout["Right Fencer"]
        print(f"--- {left} vs {right} ---")
        bout_df = cast(
            pd.DataFrame,
            main_df[
                (main_df["Left Fencer"] == left) & (main_df["Right Fencer"] == right)
            ],
        )
        metrics = MetricsCalculator(CsvFencerActionProvider(FENCER, bout_df))
        for metric in metrics.calculate():
            print(metric)
        print()


if __name__ == "__main__":
    main()
