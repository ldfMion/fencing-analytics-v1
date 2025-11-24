import pandas as pd

from data_provider import (
    DataProvider,
    FencerActionProvider,
    filter_attacks,
    filter_counter_attack_responses,
    filter_counter_attacks,
    filter_date,
    filter_left_fencer,
    filter_parries,
    filter_right_fencer,
    filter_ripostes,
    points_received_mask,
    points_scored_mask,
)


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
        df = self._df.loc[
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
        return self.get_date_fencer_action_provider(date, fencer)

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
            counter_attacks_received=lambda: count(
                pr() & filter_counter_attacks(df)
            ),
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
