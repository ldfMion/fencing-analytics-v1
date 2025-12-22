import pandas as pd
from csv_fencer_action_provider import CsvFencerActionProvider
from metrics import MetricsCalculator


def create_metrics_report(df: pd.DataFrame, fencer_name: str):
    provider = CsvFencerActionProvider(fencer_name, df)
    metrics = MetricsCalculator(provider)
    return metrics.calculate()
