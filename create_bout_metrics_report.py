from fencer_action_provider import BoutFencerActionProvider
from metrics import calculate_metrics
from models import BoutData


def create_bout_metrics_report(bout_data: BoutData, fencer_name: str):
    provider = BoutFencerActionProvider(fencer_name, bout_data)
    metrics = calculate_metrics(provider)
    return metrics
