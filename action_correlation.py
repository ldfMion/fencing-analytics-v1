import pandas as pd

from get_bouts_from_df import get_bouts_from_df


def run_no_priority_correlation(df: pd.DataFrame, fencer: str):
    bouts = get_bouts_from_df(df)
    print(bouts[0].score())
