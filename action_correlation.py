import pandas as pd

from bout_provider import get_bouts
from data_loader import load_bouts_from_df


def run_no_priority_correlation(df: pd.DataFrame, fencer: str):
    bout_data_list = load_bouts_from_df(df)
    bouts = get_bouts(bout_data_list)
    print(bouts[0].score())
