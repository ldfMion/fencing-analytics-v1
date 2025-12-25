from abc import ABC, abstractmethod
from typing import Callable, Dict, List

from actions import Action
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
    def __init__(
        self,
        name: str,
        distribution_calc: Callable[[], Dict[str, float]],
        total_calc: Callable[[], int],
    ):
        super().__init__(name)
        self._distribution_calc = distribution_calc
        self._total_calc = total_calc

    def result_to_str(self):
        dist = self._distribution_calc()
        total = self._total_calc()
        return "\n" + str.join(
            ", ",
            [
                f"{key}: {value} ({self._calc_to_str(lambda: value / total)})"
                for key, value in dist.items()
            ],
        )


class MetricsCalculator:
    def __init__(self, p: FencerActionProvider):
        self._p = p

    def calculate(self):
        return [str(metric) for metric in self._metrics()]

    def _metrics(self) -> List[Metric]:
        p = self._p
        return [
            NumericalMetric(
                "Attack Effectiveness",
                lambda: p.scored(lambda a: a.is_scoring_attack())
                / p.received(lambda a: a.is_failing_attack()),
            ),
            NumericalMetric(
                "Defense Effectiveness",
                lambda: (
                    p.scored(lambda a: a.is_scoring_defense())
                    / p.received(lambda a: a.is_failing_defense())
                ),
            ),
            NumericalMetric(
                "Riposte-to-Parry Ratio",
                lambda: p.scored(Action.is_scoring_riposte)
                / (
                    p.scored(Action.is_scoring_riposte)
                    + p.received(Action.is_failing_parry)
                ),
            ),
            NumericalMetric(
                "Counter-Attack Effectiveness",
                lambda: p.scored(Action.is_scoring_counter_attack)
                / (
                    p.scored(Action.is_scoring_counter_attack)
                    + p.received(Action.is_failing_counter_attack)
                ),
            ),
            NumericalMetric(
                # ratio of offense to defense
                "Aggression",
                lambda: (
                    p.scored(Action.is_scoring_attack)
                    + p.received(Action.is_failing_attack)
                )
                / (
                    p.received(Action.is_failing_defense)
                    + p.scored(Action.is_scoring_defense)
                ),
            ),
            NumericalMetric(
                "Attack Success Rate vs Counter-Attack",
                lambda: p.scored(Action.is_failing_counter_attack)
                / (
                    p.received(Action.is_scoring_counter_attack)
                    + p.scored(Action.is_failing_counter_attack)
                ),
            ),
            NumericalMetric(
                "Attack Success Rate vs Parry",
                lambda: p.scored(Action.is_failing_parry)
                / (
                    p.scored(Action.is_failing_parry)
                    + p.received(Action.is_scoring_riposte)
                ),
            ),
            NumericalMetric(
                "Offense EV",
                lambda: (
                    (
                        p.scored(Action.is_scoring_attack)
                        - p.received(Action.is_failing_attack)
                    )
                    / (
                        p.scored(Action.is_scoring_attack)
                        + p.received(Action.is_failing_attack)
                    )
                ),
            ),
            NumericalMetric(
                "Defense EV",
                lambda: (
                    p.scored(Action.is_scoring_defense)
                    - p.received(Action.is_failing_defense)
                )
                / (
                    p.scored(Action.is_scoring_defense)
                    + p.received(Action.is_failing_defense)
                ),
            ),
            NumericalMetric(
                "No-priority Share",  # % actions attempted without priority
                lambda: (
                    (
                        p.scored(lambda a: not a.is_scoring_priority())
                        + p.received(lambda a: not a.is_failing_priority())
                    )
                    / (p.scored(lambda a: True) + p.received(lambda a: True))
                ),
            ),
            DistributionMetric(
                "Action Distribution",
                distribution_calc=lambda: {
                    "Attacks": p.scored(Action.is_scoring_attack)
                    + p.received(Action.is_failing_attack),
                    "Counter Attacks": p.scored(Action.is_scoring_counter_attack)
                    + p.received(Action.is_failing_counter_attack),
                    "Parries": p.scored(Action.is_scoring_riposte)
                    + p.received(Action.is_failing_parry),
                },
                # this isn't the total actions because it doesn't include cards
                total_calc=lambda: p.scored(Action.is_scoring_attack)
                + p.received(Action.is_failing_attack)
                + p.scored(Action.is_scoring_counter_attack)
                + p.received(Action.is_failing_counter_attack)
                + p.scored(Action.is_scoring_riposte)
                + p.received(Action.is_failing_parry),
            ),
            DistributionMetric(
                "Scored Distribution",
                distribution_calc=lambda: {
                    "Attacks": p.scored(Action.is_scoring_attack),
                    "Counter Attacks": p.scored(Action.is_scoring_counter_attack),
                    "Ripostes": p.scored(Action.is_scoring_riposte),
                },
                total_calc=lambda: p.scored(
                    lambda a: a.is_scoring_attack()
                    and a.is_scoring_counter_attack()
                    and a.is_scoring_riposte()
                ),
            ),
            DistributionMetric(
                "Received Distribution",
                distribution_calc=lambda: {
                    "Attacks": p.received(Action.is_scoring_attack),
                    "Counter Attacks": p.received(Action.is_scoring_counter_attack),
                    "Ripostes": p.received(Action.is_scoring_riposte),
                },
                total_calc=lambda: p.received(
                    lambda a: a.is_scoring_attack()
                    and a.is_scoring_counter_attack()
                    and a.is_scoring_riposte()
                ),
            ),
        ]
