import pandas as pd

from src.data.data_loader import load_bouts_from_df
from src.domain.bout import get_bouts


def run_no_priority_correlation(df: pd.DataFrame, fencer: str):
    bout_data_list = load_bouts_from_df(df)
    bouts = get_bouts(bout_data_list)
    print(bouts[0].score())
