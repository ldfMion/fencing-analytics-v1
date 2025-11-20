from typing import Callable

import pandas as pd

from action_provider import ActionProvider
from add_touches_to_df import add_touches_to_df
from FencerAnalysis import FencerAnalysis

FILENAME = "Elite Invitationals 2025 Analytics.csv"

df = pd.read_csv(FILENAME)
df = add_touches_to_df(df)


def filter_date(df: pd.DataFrame, date: str):
    return df.loc[df["Date"] == date]


analyses: dict[str, Callable[[pd.DataFrame], pd.DataFrame]] = {
    "overall": lambda df: df,
    "Day 1": lambda df: filter_date(df, "08/11/25"),
    "Day 2": lambda df: filter_date(df, "09/11/25"),
    "4 - 4": lambda df: df.loc[(df["Left Score"] == 4) & (df["Right Score"] == 4)],
}

FENCER = "Mion"

for name, filter in analyses.items():
    provider = ActionProvider(filter(df))
    analysis = FencerAnalysis(FENCER, provider)
    print(name)
    print(analysis)
