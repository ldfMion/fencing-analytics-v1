from typing import Callable, Literal, cast

import pandas as pd

import actions

# from fencer_action_provider import FencerActionProvider


class CsvFencerActionProvider:
    def __init__(self, fencer_name: str, df: pd.DataFrame):
        self._fencer_name = fencer_name
        required_columns = {"Side", "Action", "Response", "Left Fencer", "Right Fencer"}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        self._df = cast(pd.DataFrame, df[df["Action"].notna()])

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

    """
    def attacks_scored(self):
        return count(self._points_scored_mask() & self._filter_attacks())

    def attacks_received(self):
        return count(self._points_received_mask() & self._filter_attacks())

    def counter_attacks_scored(self):
        return count(self._points_scored_mask() & self._filter_counter_attacks())

    def counter_attacks_received(self):
        return count(self._points_received_mask() & self._filter_counter_attacks())

    def ripostes_scored(self):
        return count(self._points_scored_mask() & self._filter_ripostes())

    def ripostes_received(self):
        return count(self._points_received_mask() & self._filter_ripostes())

    def attacks_received_from_parries(self):
        return count(
            self._points_received_mask()
            & self._filter_attacks()
            & self._filter_parries()
        )

    def attacks_received_from_counter_attacks(self):
        return count(
            self._points_received_mask()
            & self._filter_attacks()
            & self._filter_counter_attack_responses()
        )

    def attacks_scored_from_parries(self):
        return count(
            self._points_scored_mask() & self._filter_attacks() & self._filter_parries()
        )

    def attacks_scored_from_counter_attacks(self):
        return count(
            self._points_scored_mask()
            & self._filter_attacks()
            & self._filter_counter_attack_responses()
        )

    def attacks_scored_from_ripostes(self):
        return count(
            self._points_scored_mask()
            & self._filter_attacks()
            & self._filter_ripostes()
        )

    # --- private methods ---



    def _filter_attacks(self):
        return self._df["Action"].apply(actions.is_attack)

    def _filter_counter_attacks(self):
        return self._df["Action"].apply(actions.is_counter_attack)

    def _filter_ripostes(self):
        return self._df["Action"].apply(actions.is_riposte)

    def _filter_parries(self):
        return self._notna_response().apply(actions.is_parry)

    def _filter_counter_attack_responses(self):
        return self._notna_response().apply(actions.is_counter_attack)


    def _notna_response(self):
        return cast(pd.DataFrame, self._df[self._df["Response"].notna()])["Response"]
    """


def count(mask: pd.Series):
    return int(mask.sum())


def build_action(row: pd.Series):
    return actions.Action(
        str(row["Action"]),
        None if pd.isna(row["Response"]) else str(row["Response"]),
    )
