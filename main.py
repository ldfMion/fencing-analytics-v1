import pandas as pd

from csv_data_provider import CsvDataProvider
from fencing_analysis import FencingAnalysis
from process_df import add_touches_to_df

FILENAME = "Elite Invitationals 2025 Analytics.csv"
FENCER = "Mion"


def main():
    df = pd.read_csv(FILENAME)
    df = add_touches_to_df(df)

    data_provider = CsvDataProvider(df)

    analyses = {
        "overall": data_provider.get_fencer_action_provider(FENCER),
        "Day 1": data_provider.get_date_fencer_action_provider("08/11/25", FENCER),
        "Day 2": data_provider.get_date_fencer_action_provider("09/11/25", FENCER),
    }

    analysis = FencingAnalysis(df, analyses)
    results = analysis.run()

    for name, result in results.items():
        print(f"------- Analysis: {name} --------")
        for metric in result:
            print(metric)
        print()


if __name__ == "__main__":
    main()
