from typing import List

import pandas as pd

from src.data.constants import (
    ACTION,
    DATE,
    LEFT_FENCER,
    LEFT_SCORE,
    RESPONSE,
    RIGHT_FENCER,
    RIGHT_SCORE,
    SIDE,
)
from src.domain.actions import Action
from src.domain.models import BoutData, Touch


def load_data(touches_file: str, bouts_file: str):
    touches_df = pd.read_csv(touches_file)
    required_columns = {SIDE, ACTION, RESPONSE}
    missing = required_columns - set(touches_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    bouts_df = pd.read_csv(bouts_file)
    return touches_df, bouts_df


def add_touches_to_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds the cumulative score to each touch in the DataFrame.

    Args:
        df: The DataFrame containing the bout data.

    Returns:
        The DataFrame with the cumulative score added.
    """
    df["scored"] = df[SIDE].isin(["L", "R"]) & df[ACTION].notna()
    df["left_score_touch"] = (df[SIDE] == "L") & df["scored"]
    df["right_score_touch"] = (df[SIDE] == "R") & df["scored"]
    df["bout_id"] = df[LEFT_FENCER] + " vs " + df[RIGHT_FENCER] + " on " + df[DATE]
    df[LEFT_SCORE] = (
        df.groupby("bout_id")["left_score_touch"].cumsum() - df["left_score_touch"]
    )
    df[RIGHT_SCORE] = (
        df.groupby("bout_id")["right_score_touch"].cumsum() - df["right_score_touch"]
    )
    df = df.drop(columns=["scored", "left_score_touch", "right_score_touch", "bout_id"])
    return df


def load_bouts_from_df(df: pd.DataFrame) -> List[BoutData]:
    """
    Loads all bouts from a DataFrame.

    Args:
        df: The DataFrame containing the bout data.

    Returns:
        A list of BoutData objects.
    """
    bout_groups = df.groupby([LEFT_FENCER, RIGHT_FENCER, DATE])
    bouts = []
    for (left_fencer, right_fencer, date), bout_df in bout_groups:
        touches = []
        for _, row in bout_df.iterrows():
            action = Action(
                str(row[ACTION]),
                None if pd.isna(row[RESPONSE]) else str(row[RESPONSE]),
            )
            touch = Touch(
                action=action,
                side=row[SIDE],
                left_score=row[LEFT_SCORE],
                right_score=row[RIGHT_SCORE],
            )
            touches.append(touch)
        bout = BoutData(
            left_fencer=left_fencer,
            right_fencer=right_fencer,
            date=date,
            touches=touches,
        )
        bouts.append(bout)
    return bouts
