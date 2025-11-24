from typing import Literal

import pandas as pd

from data_provider import DataProvider, FencerActionProvider


class CsvDataProvider(DataProvider):
    def __init__(self, df: pd.DataFrame):
        self._df = df

    def get_fencer_action_provider(self, fencer_name: str) -> FencerActionProvider:
        return self._make_fencer_action_provider(self._df, fencer_name)

    def get_date_fencer_action_provider(
        self, date: str, fencer_name: str
    ) -> FencerActionProvider:
        df = self._df.loc[filter_date(self._df, date)]
        return self._make_fencer_action_provider(df, fencer_name)

    def get_bout_fencer_action_provider(
        self, date: str, fencer: str, opponent: str
    ) -> FencerActionProvider:
        df = self._df.loc[filter_date(self._df, date)]
        df = df.loc[
            (
                (
                    filter_right_fencer(self._df, fencer)
                    & filter_left_fencer(self._df, opponent)
                )
                | (
                    filter_right_fencer(self._df, opponent)
                    & filter_left_fencer(self._df, fencer)
                )
            )
        ]
        return self._make_fencer_action_provider(df, fencer)

    def _make_fencer_action_provider(
        self, df: pd.DataFrame, fencer_name: str
    ) -> FencerActionProvider:
        def count(mask: pd.Series):
            return int(mask.sum())

        def ps():
            return points_scored_mask(df, fencer_name)

        def pr():
            return points_received_mask(df, fencer_name)

        return FencerActionProvider(
            attacks_scored=lambda: count(ps() & filter_attacks(df)),
            attacks_received=lambda: count(pr() & filter_attacks(df)),
            counter_attacks_scored=lambda: count(ps() & filter_counter_attacks(df)),
            counter_attacks_received=lambda: count(pr() & filter_counter_attacks(df)),
            ripostes_scored=lambda: count(ps() & filter_ripostes(df)),
            ripostes_received=lambda: count(pr() & filter_ripostes(df)),
            attacks_received_from_parries=lambda: count(
                pr() & filter_attacks(df) & filter_parries(df)
            ),
            attacks_received_from_counter_attacks=lambda: count(
                pr() & filter_attacks(df) & filter_counter_attack_responses(df)
            ),
            attacks_scored_from_parries=lambda: count(
                ps() & filter_attacks(df) & filter_parries(df)
            ),
            attacks_scored_from_counter_attacks=lambda: count(
                ps() & filter_attacks(df) & filter_counter_attack_responses(df)
            ),
        )


def filter_date(df: pd.DataFrame, date: str):
    return df["Date"] == date


def filter_side(df: pd.DataFrame, side: Literal["L", "R"]):
    return df["Side"] == side


def filter_left_actions(df: pd.DataFrame):
    return filter_side(df, "L")


def filter_right_actions(df: pd.DataFrame):
    return filter_side(df, "R")


def filter_attacks(df: pd.DataFrame):
    return df["Action"].str.contains("A", case=True, na=False)


def filter_counter_attacks(df: pd.DataFrame):
    return df["Action"].str.contains("C", case=True, na=False)


def filter_ripostes(df: pd.DataFrame):
    return df["Action"].str.contains("R", case=True, na=False)


def filter_parries(df: pd.DataFrame):
    return df["Response"] == "P"


def filter_counter_attack_responses(df: pd.DataFrame):
    return df["Response"].str.contains("C", na=False)


def filter_left_fencer(df: pd.DataFrame, name: str):
    return df["Left Fencer"] == name


def filter_right_fencer(df: pd.DataFrame, name: str):
    return df["Right Fencer"] == name


def points_scored_mask(df: pd.DataFrame, name: str):
    left_scored = filter_left_actions(df) & filter_left_fencer(df, name)
    right_scored = filter_right_actions(df) & filter_right_fencer(df, name)
    return left_scored | right_scored


def points_received_mask(df: pd.DataFrame, name: str):
    left_received = filter_left_actions(df) & filter_right_fencer(df, name)
    right_received = filter_right_actions(df) & filter_left_fencer(df, name)
    return left_received | right_received
