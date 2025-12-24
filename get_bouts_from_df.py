import pandas as pd

from bout import Bout


def get_bouts_from_df(df: pd.DataFrame):
    only_fencers = df[["Left Fencer", "Right Fencer", "Date"]]
    unique_triples = only_fencers.drop_duplicates()
    return [
        Bout(
            row["Left Fencer"],  # pyright: ignore[reportArgumentType]
            row["Right Fencer"],  # pyright: ignore[reportArgumentType]
            row["Date"],  # pyright: ignore[reportArgumentType]
            df,
        )
        for _, row in unique_triples.iterrows()
    ]
