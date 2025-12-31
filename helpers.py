import pandas as pd

import actions


def count(mask: pd.Series) -> int:
    """
    Counts the number of True values in a boolean Series.

    Args:
        mask: A pandas Series of boolean values.

    Returns:
        The number of True values in the Series.
    """
    return int(mask.sum())


def build_action(row: pd.Series) -> actions.Action:
    """
    Builds an Action object from a DataFrame row.

    Args:
        row: A row from the fensing data DataFrame.

    Returns:
        An Action object.
    """
    response = row["Response"]
    return actions.Action(
        str(row["Action"]),
        None if response is None or pd.isna(response) else str(response),  # pyright: ignore[reportGeneralTypeIssues]
    )
