from typing import List

import pandas as pd

from bout import Bout
from bout_provider import get_bouts
from constants import DATE, LEFT_SCORE, RIGHT_SCORE
from create_bout_metrics_report import create_bout_metrics_report
from create_metrics_report import create_metrics_report
from data_loader import load_bouts_from_df
from models import BoutData


def analyze_fencer(main_df: pd.DataFrame, fencer_name: str):
    """
    Performs analysis on a fencer's performance.

    Args:
        main_df: The main DataFrame containing all bout data.
        fencer_name: The name of the fencer to analyze.
    """
    sources = {
        "overall": main_df,
        "Elites - Day 1": main_df[main_df[DATE] == "08/11/25"],
        "Elites - Day 2": main_df[main_df[DATE] == "09/11/25"],
        "Western - Day 1": main_df[main_df[DATE] == "22/11/25"],
        "Western - Day 2": main_df[main_df[DATE] == "23/11/25"],
        "4-4": main_df[(main_df[LEFT_SCORE] == 4) & (main_df[RIGHT_SCORE] == 4)],
    }

    for name, df in sources.items():
        result = create_metrics_report(df, fencer_name)
        print(f"------- Analysis: {name} --------")
        for metric in result:
            print(metric)
        print()

    bout_data_list = load_bouts_from_df(main_df)
    bouts = get_bouts(bout_data_list)
    analyze_bouts(bouts, fencer_name)


def analyze_bouts(bouts: List[Bout], fencer_name: str):
    """
    Performs analysis on a list of bouts.

    Args:
        bouts: A list of Bout objects.
        fencer_name: The name of the fencer to analyze.
    """
    print("Analyzing bouts: ")
    for bout in bouts:
        print(bout.get_summary())
        result = create_bout_metrics_report(bout._bout_data, fencer_name)
        for metric in result:
            print(metric)
        print()
