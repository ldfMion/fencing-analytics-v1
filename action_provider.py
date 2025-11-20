from typing import Literal

import pandas as pd


class ActionProvider:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def count_attacks_scored(self, fencer_name: str):
        return ActionProvider._get_attacks_scored(self.df, fencer_name).sum()

    def count_counter_attacks_scored(self, fencer_name: str):
        return ActionProvider._get_counter_attacks_scored(self.df, fencer_name).sum()

    def count_ripostes_scored(self, fencer_name: str):
        return ActionProvider._get_ripostes_scored(self.df, fencer_name).sum()

    def count_attacks_received(self, fencer_name: str):
        return ActionProvider._get_attacks_received(self.df, fencer_name).sum()

    def count_counter_attacks_received(self, fencer_name: str):
        return ActionProvider._get_counter_attacks_received(self.df, fencer_name).sum()

    def count_ripostes_received(self, fencer_name: str):
        return ActionProvider._get_ripostes_received(self.df, fencer_name).sum()

    def count_attacks_received_from_parries(self, fencer_name: str):
        return (
            ActionProvider._get_attacks_received(self.df, fencer_name)
            & ActionProvider._filter_parries(self.df)
        ).sum()

    def count_attacks_scored_on_parries(self, fencer_name: str):
        return (
            ActionProvider._get_attacks_scored(self.df, fencer_name)
            & ActionProvider._filter_parries(self.df)
        ).sum()

    def count_attacks_received_from_counter_attacks(self, fencer_name: str):
        return (
            ActionProvider._get_attacks_received(self.df, fencer_name)
            & ActionProvider._filter_counter_attack_responses(self.df)
        ).sum()

    def count_attacks_scored_on_counter_attacks(self, fencer_name: str):
        return (
            ActionProvider._get_attacks_scored(self.df, fencer_name)
            & ActionProvider._filter_counter_attack_responses(self.df)
        ).sum()

    # --- PRIVATE METHODS

    @staticmethod
    def _get_attacks_scored(df: pd.DataFrame, fencer_name: str):
        return ActionProvider._filter_points_scored(
            df, fencer_name
        ) & ActionProvider._filter_attacks(df)

    @staticmethod
    def _get_counter_attacks_scored(df: pd.DataFrame, fencer_name: str):
        return ActionProvider._filter_points_scored(
            df, fencer_name
        ) & ActionProvider._filter_counter_attacks(df)

    @staticmethod
    def _get_ripostes_scored(df: pd.DataFrame, fencer_name: str):
        return ActionProvider._filter_points_scored(
            df, fencer_name
        ) & ActionProvider._filter_ripostes(df)

    @staticmethod
    def _get_attacks_received(df: pd.DataFrame, fencer_name: str):
        return ActionProvider._filter_points_received(
            df, fencer_name
        ) & ActionProvider._filter_attacks(df)

    @staticmethod
    def _get_counter_attacks_received(df: pd.DataFrame, fencer_name: str):
        return ActionProvider._filter_points_received(
            df, fencer_name
        ) & ActionProvider._filter_counter_attacks(df)

    @staticmethod
    def _get_ripostes_received(df: pd.DataFrame, fencer_name: str):
        return ActionProvider._filter_points_received(
            df, fencer_name
        ) & ActionProvider._filter_ripostes(df)

    # --- ACTIONS

    @staticmethod
    def _filter_attacks(df: pd.DataFrame):
        return df["Action"].str.contains("A", case=True, na=False)

    @staticmethod
    def _filter_counter_attacks(df: pd.DataFrame):
        return df["Action"].str.contains("C", case=True, na=False)

    @staticmethod
    def _filter_ripostes(df: pd.DataFrame):
        return df["Action"].str.contains("R", case=True, na=False)

    # --- RESPONSES

    @staticmethod
    def _filter_parries(df: pd.DataFrame):
        return df["Response"] == "P"

    @staticmethod
    def _filter_counter_attack_responses(df: pd.DataFrame):
        return df["Response"].str.contains("C")

    # --- SIDE HELPERS

    @staticmethod
    def _filter_points_scored(df: pd.DataFrame, fencer_name: str):
        left_mask = ActionProvider._filter_left_actions(
            df
        ) & ActionProvider._filter_left_fencer(df, fencer_name)
        right_mask = ActionProvider._filter_right_actions(
            df
        ) & ActionProvider._filter_right_fencer(df, fencer_name)
        return left_mask | right_mask

    @staticmethod
    def _filter_points_received(df: pd.DataFrame, fencer_name: str):
        left_mask = ActionProvider._filter_left_actions(
            df
        ) & ActionProvider._filter_right_fencer(df, fencer_name)
        right_mask = ActionProvider._filter_right_actions(
            df
        ) & ActionProvider._filter_left_fencer(df, fencer_name)
        return left_mask | right_mask

    @staticmethod
    def _filter_left_fencer(df: pd.DataFrame, fencer_name: str):
        return df["Left Fencer"] == fencer_name

    @staticmethod
    def _filter_right_fencer(df: pd.DataFrame, fencer_name: str):
        return df["Right Fencer"] == fencer_name

    @staticmethod
    def _filter_left_actions(df: pd.DataFrame):
        return ActionProvider._filter_side(df, "L")

    @staticmethod
    def _filter_right_actions(df: pd.DataFrame):
        return ActionProvider._filter_side(df, "R")

    @staticmethod
    def _filter_side(df: pd.DataFrame, side: Literal["R", "L"]):
        return df["Side"] == side
