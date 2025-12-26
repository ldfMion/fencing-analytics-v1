from fencer_action_provider import BoutFencerActionProvider
from metrics import MetricsCalculator
from models import BoutData


def create_bout_metrics_report(bout_data: BoutData, fencer_name: str):
    provider = BoutFencerActionProvider(fencer_name, bout_data)
    metrics = MetricsCalculator(provider)
    return metrics.calculate()
