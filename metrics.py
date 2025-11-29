from abc import ABC, abstractmethod
from typing import Callable, Dict, List

from fencer_action_provider import FencerActionProvider


class Metric(ABC):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return f"{self._name}: {self.result_to_str()}"

    def _calc_to_str(self, calculation: Callable[[], float]):
        try:
            return str(round(calculation(), 2))
        except ZeroDivisionError:
            return "N/A"

    @abstractmethod
    def result_to_str(self) -> str: ...


class NumericalMetric(Metric):
    def __init__(self, name: str, calculation: Callable[[], float]):
        super().__init__(name)
        self._calculation = calculation

    def result_to_str(self) -> str:
        return self._calc_to_str(self._calculation)


class DistributionMetric(Metric):
    def __init__(self, name: str, calculation: Callable[[], Dict[str, float]]):
        super().__init__(name)
        self._calculation = calculation

    def result_to_str(self):
        return "\n" + str.join(
            ", ", [f"{key}: {value}" for key, value in self._calculation().items()]
        )


class MetricsCalculator:
    def __init__(self, p: FencerActionProvider):
        self._p = p

    def calculate(self):
        return [str(metric) for metric in self._metrics()]

    def _metrics(self) -> List[Metric]:
        return [
            NumericalMetric(
                "Attack Effectiveness",
                lambda: self._p.attacks_scored()
                / (self._p.counter_attacks_received() + self._p.ripostes_received()),
            ),
            NumericalMetric(
                "Defense Effectiveness",
                lambda: (self._p.counter_attacks_scored() + self._p.ripostes_scored())
                / self._p.attacks_received(),
            ),
            NumericalMetric(
                "Riposte-to-Parry Ratio",
                lambda: self._p.ripostes_scored()
                / (self._p.ripostes_scored() + self._p.attacks_received_from_parries()),
            ),
            NumericalMetric(
                "Counter-Attack Effectiveness",
                lambda: self._p.counter_attacks_scored()
                / (
                    self._p.counter_attacks_scored()
                    + self._p.attacks_received_from_counter_attacks()
                ),
            ),
            NumericalMetric(
                "Aggression",
                lambda: (
                    self._p.attacks_scored()
                    + self._p.counter_attacks_received()
                    + self._p.ripostes_received()
                )
                / (
                    self._p.counter_attacks_scored()
                    + self._p.attacks_received_from_counter_attacks()
                    + self._p.ripostes_scored()
                    + self._p.attacks_received_from_parries()
                ),
            ),
            NumericalMetric(
                "Attack vs Counter-Attack Efficiency",
                lambda: self._p.attacks_scored_from_counter_attacks()
                / (
                    self._p.counter_attacks_received()
                    + self._p.attacks_scored_from_counter_attacks()
                ),
            ),
            NumericalMetric(
                "Attack vs Parry Efficiency",
                lambda: self._p.attacks_scored_from_parries()
                / (self._p.attacks_scored_from_parries() + self._p.ripostes_received()),
            ),
            NumericalMetric(
                "Offense EV",
                lambda: (
                    self._p.attacks_scored()
                    / (
                        self._p.attacks_scored()
                        + self._p.counter_attacks_received()
                        + self._p.ripostes_received()
                    )
                )
                - (
                    (self._p.counter_attacks_received() + self._p.ripostes_received())
                    / (
                        self._p.attacks_scored()
                        + self._p.counter_attacks_received()
                        + self._p.ripostes_received()
                    )
                ),
            ),
            NumericalMetric(
                "Defense EV",
                lambda: (
                    (self._p.counter_attacks_scored() + self._p.ripostes_scored())
                    / (
                        self._p.counter_attacks_scored()
                        + self._p.ripostes_scored()
                        + self._p.attacks_received()
                    )
                )
                - (
                    self._p.attacks_received()
                    / (
                        self._p.counter_attacks_scored()
                        + self._p.ripostes_scored()
                        + self._p.attacks_received()
                    )
                ),
            ),
            DistributionMetric(
                "Action Distribution",
                lambda: {
                    "Attacks": self._p.attacks_scored()
                    + self._p.counter_attacks_received()
                    + self._p.ripostes_received(),
                    "Counter Attacks": self._p.attacks_received_from_counter_attacks()
                    + self._p.counter_attacks_scored(),
                    "Parries": self._p.ripostes_scored()
                    + self._p.attacks_received_from_parries(),
                },
            ),
            DistributionMetric(
                "Scored Distribution",
                lambda: {
                    "Attacks": self._p.attacks_scored(),
                    "Counter Attacks": self._p.counter_attacks_scored(),
                    "Ripostes": self._p.ripostes_scored(),
                },
            ),
            DistributionMetric(
                "Received Distribution",
                lambda: {
                    "Attacks": self._p.attacks_received(),
                    "Counter Attacks": self._p.counter_attacks_received(),
                    "Ripostes": self._p.ripostes_received(),
                },
            ),
        ]
