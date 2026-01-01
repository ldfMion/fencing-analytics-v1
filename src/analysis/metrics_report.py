import pandas as pd

from src.analysis.metrics import calculate_metrics
from src.data.csv_fencer_action_provider import CsvFencerActionProvider
from src.data.fencer_action_provider import (
    BoutFencerActionProvider,
)
from src.domain.models import BoutData


def create_bout_metrics_report(bout_data: BoutData, fencer_name: str):
    provider = BoutFencerActionProvider(fencer_name, bout_data)
    metrics = calculate_metrics(provider)
    return metrics


def create_metrics_report(df: pd.DataFrame, fencer_name: str):
    provider = CsvFencerActionProvider(fencer_name, df)
    metrics = calculate_metrics(provider)
    return metrics
