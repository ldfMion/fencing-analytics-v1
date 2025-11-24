from typing import Dict, List
import pandas as pd

from data_provider import FencerActionProvider
from metrics import Metrics


class FencingAnalysis:
    def __init__(self, df: pd.DataFrame, analyses: Dict[str, FencerActionProvider]):
        self._df = df
        self._analyses = analyses

    def run(self) -> Dict[str, List[str]]:
        results = {}
        for name, provider in self._analyses.items():
            metrics = Metrics(provider)
            results[name] = [str(metric) for metric in metrics.calculate()]
        return results
