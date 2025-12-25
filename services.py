import pandas as pd

from create_metrics_report import create_metrics_report
from get_bouts_from_df import get_bouts_from_df


def analyze_fencer(main_df: pd.DataFrame, fencer_name: str):
    sources = {
        "overall": main_df,
        "Day 1": main_df[main_df["Date"] == "08/11/25"],
        "Day 2": main_df[main_df["Date"] == "09/11/25"],
        "4-4": main_df[(main_df["Left Score"] == 4) & (main_df["Right Score"] == 4)],
    }

    for name, df in sources.items():
        result = create_metrics_report(df, fencer_name)
        print(f"------- Analysis: {name} --------")
        for metric in result:
            print(metric)
        print()

    bouts = get_bouts_from_df(main_df)
    print("Analyzing bouts: ")
    for bout in bouts:
        print(bout.get_summary())
        for metric in bout.get_metrics(bout.left == fencer_name):
            print(metric)
        print()
