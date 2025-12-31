import pandas as pd

from csv_fencer_action_provider import CsvFencerActionProvider
from metrics import calculate_metrics


def create_metrics_report(df: pd.DataFrame, fencer_name: str):
    provider = CsvFencerActionProvider(fencer_name, df)
    metrics = calculate_metrics(provider)
    return metrics
