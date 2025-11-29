import pandas as pd

from csv_fencer_action_provider import CsvFencerActionProvider
from fencing_analysis import FencingAnalysis
from metrics import Metrics
from process_df import add_touches_to_df

FILENAME = "Elite Invitationals 2025 Analytics.csv"
FENCER = "Mion"


def main():
    main_df = pd.read_csv(FILENAME)
    main_df = add_touches_to_df(main_df)

    sources = {
        "overall": main_df,
        "Day 1": main_df[main_df["Date"] == "08/11/25"],
        "Day 2": main_df[main_df["Date"] == "09/11/25"],
    }

    for name, df in sources.items():
        metrics = Metrics(CsvFencerActionProvider(FENCER, df))
        analysis = FencingAnalysis(df, metrics)
        result = analysis.run()
        print(f"------- Analysis: {name} --------")
        for metric in result:
            print(metric)
        print()


if __name__ == "__main__":
    main()
