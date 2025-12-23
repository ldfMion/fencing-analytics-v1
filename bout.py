from typing import cast

import pandas as pd

from csv_fencer_action_provider import CsvFencerActionProvider
from metrics import MetricsCalculator
from services import create_metrics_report


class Bout:
    left: str
    right: str
    date: str
    bout_df: pd.DataFrame

    def __init__(self, left: str, right: str, date: str, main_df: pd.DataFrame):
        self.left = left
        self.right = right
        self.date = date
        self.bout_df = cast(
            pd.DataFrame,
            main_df[
                (main_df["Left Fencer"] == self.left)
                & (main_df["Right Fencer"] == self.right)
            ],
        )

    def get_summary(self) -> str:
        summary = f"{self.left} vs {self.right} ({self.date})---\n\n"
        for i, row in self.bout_df.iterrows():
            if pd.notna(row["Action"]):  # pyright: ignore[reportGeneralTypeIssues]
                text = f"{row['Action']}"
                if pd.notna(row["Response"]):  # pyright: ignore[reportGeneralTypeIssues]
                    text += f" ({row['Response']})"
                if row["Side"] == "R":
                    pad = len(self.left) + 4 + len(text)
                    text = text.rjust(pad, " ")
                summary += text + "\n"
        return summary

    def get_metrics(self, left_fencer: bool):
        fencer = self.left if left_fencer else self.right
        return create_metrics_report(self.bout_df, fencer)
