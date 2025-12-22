import pandas as pd
from config import FENCER, FILENAME
from process_df import add_touches_to_df, get_bouts_from_df
from services import create_metrics_report


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
        result = create_metrics_report(df, FENCER)
        print(f"------- Analysis: {name} --------")
        for metric in result:
            print(metric)
        print()

    bouts = get_bouts_from_df(main_df)
    print("Analyzing bouts: ")
    for bout in bouts:
        print(bout.get_summary())
        for metric in bout.get_metrics(bout.left == FENCER):
            print(metric)
        print()


if __name__ == "__main__":
    main()
