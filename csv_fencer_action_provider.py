from typing import Callable, List, Literal, Tuple, cast

import pandas as pd

import actions
from fencer_action_provider import (
    ActionOutcome,
    FencerActionProvider,
    OrderedFencerActionProvider,
)

YELLOW_CARD = "yc"
RED_CARD = "rc"


class CsvFencerActionProvider(FencerActionProvider):
    def __init__(self, fencer_name: str, df: pd.DataFrame):
        self._fencer_name = fencer_name
        required_columns = {"Side", "Action", "Response", "Left Fencer", "Right Fencer"}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        self._df = cast(
            pd.DataFrame,
            df[
                df["Action"].notna()
                & (df["Action"] != YELLOW_CARD)
                & (df["Action"] != RED_CARD)
            ],
        )

    def scored(self, action_filter: Callable[[actions.Action], bool]):
        return count(self._points_scored_mask() & self._filter_actions(action_filter))

    def received(self, action_filter: Callable[[actions.Action], bool]):
        return count(self._points_received_mask() & self._filter_actions(action_filter))

    def _filter_actions(self, action_filter: Callable[[actions.Action], bool]):
        return self._df.apply(lambda row: action_filter(build_action(row)), axis=1)

    def _points_scored_mask(self):
        left_scored = self._filter_left_actions() & self._filter_left_fencer()
        right_scored = self._filter_right_actions() & self._filter_right_fencer()
        return left_scored | right_scored

    def _points_received_mask(self):
        left_received = self._filter_left_actions() & self._filter_right_fencer()
        right_received = self._filter_right_actions() & self._filter_left_fencer()
        return left_received | right_received

    def _filter_left_actions(self):
        return self._filter_side("L")

    def _filter_right_actions(self):
        return self._filter_side("R")

    def _filter_left_fencer(self):
        return self._df["Left Fencer"] == self._fencer_name

    def _filter_right_fencer(self):
        return self._df["Right Fencer"] == self._fencer_name

    def _filter_side(self, side: Literal["L", "R"]):
        return self._df["Side"] == side


def count(mask: pd.Series):
    return int(mask.sum())


def build_action(row: pd.Series):
    return actions.Action(
        str(row["Action"]),
        None if pd.isna(row["Response"]) else str(row["Response"]),  # pyright: ignore[reportGeneralTypeIssues]
    )


class CsvOrderedFencerActionProvider(
    CsvFencerActionProvider, OrderedFencerActionProvider
):
    def __init__(self, fencer_name: str, df: pd.DataFrame):
        super().__init__(fencer_name, df)

    def get_actions(
        self,
    ) -> List[
        Tuple[
            Tuple[actions.Action, ActionOutcome], Tuple[actions.Action, ActionOutcome]
        ]
    ]:
        return list(
            map(
                lambda pair: (
                    (
                        build_action(pair[0]),
                        ActionOutcome.FOR
                        if pair[0]["Side"] == "L"
                        and pair[0]["Left Fencer"] == self._fencer_name
                        else ActionOutcome.AGAINST,
                    ),
                    (
                        build_action(pair[1]),
                        ActionOutcome.FOR
                        if pair[1]["Side"] == "L"
                        and pair[1]["Left Fencer"] == self._fencer_name
                        else ActionOutcome.AGAINST,
                    ),
                ),
                filter(
                    lambda pair: pair[0]["Left Fencer"] == pair[1]["Left Fencer"]
                    and pair[0]["Right Fencer"] == pair[1]["Right Fencer"]
                    and pair[0]["Date"] == pair[1]["Date"],
                    zip(
                        self._df.iloc[:-1].to_dict("records"),
                        self._df.iloc[1:].to_dict("records"),
                    ),
                ),
            )
        )
