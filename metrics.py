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
        if total == 0:
            return "N/A"
        return "\n" + str.join(
            ", ",
            [
                f"{key}: {value} ({self._calc_to_str(lambda: value / total)})"
                for key, value in dist.items()
            ],
        )


def attack_effectiveness(p: FencerActionProvider) -> float:
    scored = p.scored(Action.is_scoring_attack)
    received = p.received(Action.is_failing_attack)
    return scored / (scored + received)


def defense_effectiveness(p: FencerActionProvider) -> float:
    scored = p.scored(Action.is_scoring_defense)
    received = p.received(Action.is_failing_defense)
    return scored / (scored + received)


def riposte_to_parry_ratio(p: FencerActionProvider) -> float:
    """Calculates the ratio of successful ripostes to total parries."""
    # isn't counter counter ripostes I think
    return p.scored(Action.is_scoring_riposte) / (
        p.scored(Action.is_scoring_riposte) + p.received(Action.is_failing_parry)
    )


def counter_attack_effectiveness(p: FencerActionProvider) -> float:
    """Calculates the effectiveness of counter-attacks."""
    return p.scored(Action.is_scoring_counter_attack) / (
        p.scored(Action.is_scoring_counter_attack)
        + p.received(Action.is_failing_counter_attack)
    )


def aggression(p: FencerActionProvider) -> float:
    """Calculates the ratio of offensive actions to defensive actions."""
    return (
        p.scored(Action.is_scoring_attack) + p.received(Action.is_failing_attack)
    ) / (p.received(Action.is_failing_defense) + p.scored(Action.is_scoring_defense))


def attack_success_rate_vs_counter_attack(p: FencerActionProvider) -> float:
    """Calculates the success rate of attacks against counter-attacks."""
    return p.scored(Action.is_failing_counter_attack) / (
        p.received(Action.is_scoring_counter_attack)
        + p.scored(Action.is_failing_counter_attack)
    )


def attack_success_rate_vs_parry(p: FencerActionProvider) -> float:
    """Calculates the success rate of attacks against parries."""
    return p.scored(Action.is_failing_parry) / (
        p.scored(Action.is_failing_parry) + p.received(Action.is_scoring_riposte)
    )


def offense_ev(p: FencerActionProvider) -> float:
    """Calculates the expected value of offensive actions."""
    return (
        p.scored(Action.is_scoring_attack) - p.received(Action.is_failing_attack)
    ) / (p.scored(Action.is_scoring_attack) + p.received(Action.is_failing_attack))


def defense_ev(p: FencerActionProvider) -> float:
    """Calculates the expected value of defensive actions."""
    return (
        p.scored(Action.is_scoring_defense) - p.received(Action.is_failing_defense)
    ) / (p.scored(Action.is_scoring_defense) + p.received(Action.is_failing_defense))


def no_priority_share(p: FencerActionProvider) -> float:
    """Calculates the percentage of actions attempted without priority."""
    return (
        p.scored(lambda a: not a.is_scoring_priority())
        + p.received(lambda a: not a.is_failing_priority())
    ) / (p.scored(lambda a: True) + p.received(lambda a: True))


class MetricsCalculator:
    def __init__(self, p: FencerActionProvider):
        self._p = p
        self._metric_functions = [
            attack_effectiveness,
            defense_effectiveness,
            riposte_to_parry_ratio,
            counter_attack_effectiveness,
            aggression,
            attack_success_rate_vs_counter_attack,
            attack_success_rate_vs_parry,
            offense_ev,
            defense_ev,
            no_priority_share,
        ]

    def calculate(self) -> List[str]:
        metrics = []
        for func in self._metric_functions:
            name = func.__name__.replace("_", " ").title()
            metric = NumericalMetric(name, lambda f=func: f(self._p))
            metrics.append(str(metric))

        # Add distribution metrics separately
        metrics.extend(self._get_distribution_metrics())
        return metrics

    def _get_distribution_metrics(self) -> List[str]:
        p = self._p
        distribution_metrics = [
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
                total_calc=lambda: p.scored(lambda a: True),
            ),
            DistributionMetric(
                "Received Distribution",
                distribution_calc=lambda: {
                    "Attacks": p.received(Action.is_scoring_attack),
                    "Counter Attacks": p.received(Action.is_scoring_counter_attack),
                    "Ripostes": p.received(Action.is_scoring_riposte),
                },
                total_calc=lambda: p.received(lambda a: True),
            ),
        ]
        return [str(metric) for metric in distribution_metrics]
