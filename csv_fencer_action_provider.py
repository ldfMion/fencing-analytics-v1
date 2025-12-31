from typing import Callable, List, Literal, Tuple, cast

import pandas as pd

import actions
from constants import (
    ACTION,
    DATE,
    LEFT_FENCER,
    RESPONSE,
    RIGHT_FENCER,
    SIDE,
)
from fencer_action_provider import (
    ActionOutcome,
    FencerActionProvider,
    OrderedFencerActionProvider,
)
from helpers import build_action, count

YELLOW_CARD = "yc"
RED_CARD = "rc"


class CsvFencerActionProvider(FencerActionProvider):
    """
    Provides fencing actions from a CSV file.
    """

    def __init__(self, fencer_name: str, df: pd.DataFrame):
        """
        Initializes the CsvFencerActionProvider.

        Args:
            fencer_name: The name of the fencer to analyze.
            df: The DataFrame containing the fencing data.
        """
        self._fencer_name = fencer_name
        required_columns = {SIDE, ACTION, RESPONSE, LEFT_FENCER, RIGHT_FENCER}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        self._df = cast(
            pd.DataFrame,
            df[
                df[ACTION].notna()
                & (df[ACTION] != YELLOW_CARD)
                & (df[ACTION] != RED_CARD)
            ],
        )

    def scored(self, action_filter: Callable[[actions.Action], bool]) -> int:
        """
        Counts the number of times the fencer scored with a specific action.

        Args:
            action_filter: A function that returns True if the action matches the filter.

        Returns:
            The number of times the fencer scored with the specified action.
        """
        # print("getting scored")
        return count(self._points_scored_mask() & self._filter_actions(action_filter))

    def received(self, action_filter: Callable[[actions.Action], bool]) -> int:
        """
        Counts the number of times the fencer received a touch with a specific action.

        Args:
            action_filter: A function that returns True if the action matches the filter.

        Returns:
            The number of times the fencer received a touch with the specified action.
        """
        # print("getting received")
        return count(self._points_received_mask() & self._filter_actions(action_filter))

    def _filter_actions(
        self, action_filter: Callable[[actions.Action], bool]
    ) -> pd.Series:
        return self._df.apply(
            lambda row: self._handle_action_row(row, action_filter), axis=1
        )  # pyright: ignore[reportReturnType]

    def _handle_action_row(self, row, action_filter):
        action = build_action(row)
        result = action_filter(action)
        # if result:
        #     print(action)
        return result

    def _points_scored_mask(self) -> pd.Series:
        left_scored = self._filter_left_actions() & self._filter_left_fencer()
        right_scored = self._filter_right_actions() & self._filter_right_fencer()
        return left_scored | right_scored

    def _points_received_mask(self) -> pd.Series:
        left_received = self._filter_left_actions() & self._filter_right_fencer()
        right_received = self._filter_right_actions() & self._filter_left_fencer()
        return left_received | right_received

    def _filter_left_actions(self) -> pd.Series:
        return self._filter_side("L")

    def _filter_right_actions(self) -> pd.Series:
        return self._filter_side("R")

    def _filter_left_fencer(self) -> pd.Series:
        return self._df[LEFT_FENCER] == self._fencer_name

    def _filter_right_fencer(self) -> pd.Series:
        return self._df[RIGHT_FENCER] == self._fencer_name

    def _filter_side(self, side: Literal["L", "R"]) -> pd.Series:
        return self._df[SIDE] == side


class CsvOrderedFencerActionProvider(
    CsvFencerActionProvider, OrderedFencerActionProvider
):
    """
    Provides ordered fencing actions from a CSV file.
    """

    def get_actions(
        self,
    ) -> List[
        Tuple[
            Tuple[actions.Action, ActionOutcome], Tuple[actions.Action, ActionOutcome]
        ]
    ]:
        """
        Gets a list of action pairs from the fencing data.

        Returns:
            A list of tuples, where each tuple contains two tuples of (Action, ActionOutcome).
        """
        action_pairs = []
        for i in range(len(self._df) - 1):
            row1 = self._df.iloc[i]
            row2 = self._df.iloc[i + 1]

            if (
                row1[LEFT_FENCER] == row2[LEFT_FENCER]
                and row1[RIGHT_FENCER] == row2[RIGHT_FENCER]
                and row1[DATE] == row2[DATE]
            ):
                action1 = build_action(row1)
                outcome1 = (
                    ActionOutcome.FOR
                    if (row1[SIDE] == "L" and row1[LEFT_FENCER] == self._fencer_name)
                    or (row1[SIDE] == "R" and row1[RIGHT_FENCER] == self._fencer_name)
                    else ActionOutcome.AGAINST
                )

                action2 = build_action(row2)
                outcome2 = (
                    ActionOutcome.FOR
                    if (row2[SIDE] == "L" and row2[LEFT_FENCER] == self._fencer_name)
                    or (row2[SIDE] == "R" and row2[RIGHT_FENCER] == self._fencer_name)
                    else ActionOutcome.AGAINST
                )

                action_pairs.append(((action1, outcome1), (action2, outcome2)))
        return action_pairs
