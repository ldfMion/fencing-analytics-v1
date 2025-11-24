from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Literal

import pandas as pd

IntFunc = Callable[[], int]


@dataclass
class FencerActionProvider:
    attacks_scored: IntFunc
    attacks_received: IntFunc
    counter_attacks_scored: IntFunc
    counter_attacks_received: IntFunc
    ripostes_scored: IntFunc
    ripostes_received: IntFunc
    attacks_received_from_parries: IntFunc
    attacks_received_from_counter_attacks: IntFunc
    attacks_scored_from_parries: IntFunc
    attacks_scored_from_counter_attacks: IntFunc


class DataProvider(ABC):
    @abstractmethod
    def get_fencer_action_provider(self, fencer_name: str) -> FencerActionProvider:
        ...

    @abstractmethod
    def get_date_fencer_action_provider(
        self, date: str, fencer_name: str
    ) -> FencerActionProvider:
        ...

    @abstractmethod
    def get_bout_fencer_action_provider(
        self, date: str, fencer: str, opponent: str
    ) -> FencerActionProvider:
        ...


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
