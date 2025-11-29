from typing import List

import pandas as pd

from metrics import Metrics


class FencingAnalysis:
    def __init__(self, df: pd.DataFrame, metrics: Metrics):
        self._df = df
        self._metrics = metrics

    def run(self) -> List[str]:
        results = [str(metric) for metric in self._metrics.calculate()]
        return results
