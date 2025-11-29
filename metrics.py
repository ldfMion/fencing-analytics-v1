from typing import Callable, List

from fencer_action_provider import FencerActionProvider


class Metric:
    def __init__(self, name: str, calculation: Callable[[], float]):
        self._name = name
        self._calculation = calculation

    def __str__(self) -> str:
        try:
            value = self._calculation()
            return f"{self._name}: {round(value, 2)}"
        except ZeroDivisionError:
            return f"{self._name}: N/A"


class MetricsCalculator:
    def __init__(self, p: FencerActionProvider):
        self._p = p

    def calculate(self):
        return [str(metric) for metric in self._metrics()]

    def _metrics(self) -> List[Metric]:
        return [
            Metric(
                "Attack Effectiveness",
                lambda: self._p.attacks_scored()
                / (self._p.counter_attacks_received() + self._p.ripostes_received()),
            ),
            Metric(
                "Defense Effectiveness",
                lambda: (self._p.counter_attacks_scored() + self._p.ripostes_scored())
                / self._p.attacks_received(),
            ),
            Metric(
                "Riposte-to-Parry Ratio",
                lambda: self._p.ripostes_scored()
                / (self._p.ripostes_scored() + self._p.attacks_received_from_parries()),
            ),
            Metric(
                "Counter-Attack Effectiveness",
                lambda: self._p.counter_attacks_scored()
                / (
                    self._p.counter_attacks_scored()
                    + self._p.attacks_received_from_counter_attacks()
                ),
            ),
            Metric(
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
            Metric(
                "Attack vs Counter-Attack Efficiency",
                lambda: self._p.attacks_scored_from_counter_attacks()
                / (
                    self._p.counter_attacks_received()
                    + self._p.attacks_scored_from_counter_attacks()
                ),
            ),
            Metric(
                "Attack vs Parry Efficiency",
                lambda: self._p.attacks_scored_from_parries()
                / (self._p.attacks_scored_from_parries() + self._p.ripostes_received()),
            ),
            Metric(
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
            Metric(
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
        ]
