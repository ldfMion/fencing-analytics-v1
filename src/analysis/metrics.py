from typing import Callable

from src.data.fencer_action_provider import FencerActionProvider
from src.domain.actions import (
    ActionType,
    DefensiveAlternative,
    Priority,
    TacticalIntent,
)


def format_metric(
    name: str,
    formula: Callable[[FencerActionProvider], float],
    provider: FencerActionProvider,
) -> str:
    """Format a numerical metric as a string, handling division by zero."""
    try:
        # print(f"calculating {name}")
        value = formula(provider)
        return f"{name}: {round(value, 2)}"
    except ZeroDivisionError:
        return f"{name}: N/A"


def format_distribution(
    name: str,
    dist_fn: Callable[[FencerActionProvider], dict[str, int]],
    provider: FencerActionProvider,
) -> str:
    """Format a distribution metric with counts and percentages."""
    # print(f"calculating distribution {name}")
    dist = dist_fn(provider)
    total = sum(dist.values())

    if total == 0:
        return f"{name}: N/A"

    parts = [
        f"{key}: {value} ({round(value / total, 2)})" for key, value in dist.items()
    ]
    return f"{name}:\n" + ", ".join(parts)


def proportion(a: int, b: int) -> float:
    return a / (a + b)


def ratio(a: int, b: int) -> float:
    return a / b


# def numerical_metric(name: str, formula: Callable[[FencerActionProvider], float]):
#     return lambda p: format_metric(name, formula, p)


# def distribution_metric(
#     name: str, dist_fn: Callable[[FencerActionProvider], dict[str, int]]
# ):
#     return lambda p: format_distribution(name, dist_fn, p)


# # Define all numerical metrics

# METRICS: dict[str, list[Callable[[FencerActionProvider], str]]] = {
#     "Behavior Metrics": [],
#     "Performance Metrics": [],
# }

METRICS: dict[str, Callable[[FencerActionProvider], float]] = {
    "Offense Effectiveness": lambda p: proportion(
        p.scored(lambda a: a.scoring_tactical_intent_is(TacticalIntent.OFFENSIVE)),
        p.received(lambda a: a.receiving_tactical_intent_is(TacticalIntent.OFFENSIVE)),
    ),
    "Defense Effectiveness": lambda p: proportion(
        p.scored(lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE)),
        p.received(lambda a: a.receiving_tactical_intent_is(TacticalIntent.DEFENSIVE)),
    ),
    # percentage of counter attacks that are successful
    "Counter Attack Effectiveness": lambda p: proportion(
        p.scored(lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)),
        p.received(lambda a: a.receiving_action_type_is(ActionType.COUNTER_ATTACK)),
    ),
    "Offensive Volume": lambda p: proportion(
        p.scored(lambda a: a.scoring_tactical_intent_is(TacticalIntent.OFFENSIVE))
        + p.received(
            lambda a: a.receiving_tactical_intent_is(TacticalIntent.OFFENSIVE)
        ),
        p.scored(lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE))
        + p.received(
            lambda a: a.receiving_tactical_intent_is(TacticalIntent.DEFENSIVE)
        ),
    ),
    "No Priority Share": lambda p: proportion(
        p.scored(lambda a: a.scoring_priority_is(Priority.WITHOUT_PRIORITY))
        + p.received(lambda a: a.receiving_priority_is(Priority.WITHOUT_PRIORITY)),
        p.scored(lambda a: a.scoring_priority_is(Priority.WITH_PRIORITY))
        + p.received(lambda a: a.receiving_priority_is(Priority.WITH_PRIORITY)),
    ),
    "Attack Success Rate vs Counter Attack": lambda p: proportion(
        p.scored(lambda a: a.receiving_action_type_is(ActionType.COUNTER_ATTACK)),
        p.received(lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)),
    ),
    "Attack Success Rate vs Parry": lambda p: proportion(
        p.scored(lambda a: a.receiving_action_type_is(ActionType.PARRY)),
        p.received(lambda a: a.scoring_action_type_is(ActionType.PARRY)),
    ),
    "Counter Attack Success Rate": lambda p: proportion(
        p.scored(lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)),
        p.received(lambda a: a.receiving_action_type_is(ActionType.COUNTER_ATTACK)),
    ),
    "Riposte Success Rate": lambda p: proportion(
        p.scored(lambda a: a.scoring_action_type_is(ActionType.PARRY)),
        p.received(lambda a: a.receiving_action_type_is(ActionType.PARRY)),
    ),
    "Attack Strength": lambda p: ratio(
        p.scored(lambda a: a.scoring_action_type_is(ActionType.ATTACK)),
        p.received(lambda a: a.scoring_action_type_is(ActionType.ATTACK)),
    ),
    "Parry Strength": lambda p: ratio(
        p.scored(lambda a: a.scoring_action_type_is(ActionType.PARRY)),
        p.received(lambda a: a.scoring_action_type_is(ActionType.PARRY)),
    ),
    "Counter Attack Strength": lambda p: ratio(
        p.scored(lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)),
        p.received(lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)),
    ),
}

DISTRIBUTIONS: dict[str, Callable[[FencerActionProvider], dict[str, int]]] = {
    "Action Distribution": lambda p: {
        "Attacks": p.scored(lambda a: a.scoring_action_type_is(ActionType.ATTACK))
        + p.received(lambda a: a.receiving_action_type_is(ActionType.ATTACK)),
        "Counter Attacks": p.scored(
            lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)
        )
        + p.received(lambda a: a.receiving_action_type_is(ActionType.COUNTER_ATTACK)),
        "Ripostes": p.scored(lambda a: a.scoring_action_type_is(ActionType.PARRY))
        + p.received(lambda a: a.receiving_action_type_is(ActionType.PARRY)),
    },
    "Received Distribution": lambda p: {
        "Attacks": p.received(lambda a: a.scoring_action_type_is(ActionType.ATTACK)),
        "Counter Attacks": p.received(
            lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)
        ),
        "Ripostes": p.received(lambda a: a.scoring_action_type_is(ActionType.PARRY)),
    },
    "Scored Distribution": lambda p: {
        "Attacks": p.scored(lambda a: a.scoring_action_type_is(ActionType.ATTACK)),
        "Counter Attacks": p.scored(
            lambda a: a.scoring_action_type_is(ActionType.COUNTER_ATTACK)
        ),
        "Ripostes": p.scored(lambda a: a.scoring_action_type_is(ActionType.PARRY)),
    },
    "Defense Distribution": lambda p: {
        "Parry": p.scored(
            lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.scoring_defensive_alternative_is(DefensiveAlternative.PARRY)
        )
        + p.received(
            lambda a: a.receiving_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.receiving_defensive_alternative_is(DefensiveAlternative.PARRY)
        ),
        "Counter Attack": p.scored(
            lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.scoring_defensive_alternative_is(DefensiveAlternative.COUNTER_ATTACK)
        )
        + p.received(
            lambda a: a.receiving_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.receiving_defensive_alternative_is(
                DefensiveAlternative.COUNTER_ATTACK
            )
        ),
        "Attack on Prep": p.scored(
            lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.scoring_defensive_alternative_is(DefensiveAlternative.ATTACK_ON_PREP)
        )
        + p.received(
            lambda a: a.receiving_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.receiving_defensive_alternative_is(
                DefensiveAlternative.ATTACK_ON_PREP
            )
        ),
        "Defense with Distance": p.scored(
            lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.scoring_defensive_alternative_is(
                DefensiveAlternative.DEFENSE_WITH_DISTANCE
            )
        ),
        "Point in Line": p.scored(
            lambda a: a.scoring_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.scoring_defensive_alternative_is(DefensiveAlternative.LINE)
        )
        + p.received(
            lambda a: a.receiving_tactical_intent_is(TacticalIntent.DEFENSIVE)
            and a.receiving_defensive_alternative_is(DefensiveAlternative.LINE)
        ),
    },
    # "Parry Outcomes": lambda p: {
    #     "Riposte Hits": p.scored(
    #         lambda a: a.classify_scoring(action_type=ActionType.PARRY)
    #     ),
    #     # todo: separate attacks and renewals
    #     "Attack or Renewal Hits": p.received(
    #         lambda a: a.classify_receiving(action_type=ActionType.ATTACK)
    #     ),
    #     "Opp Counter Riposte Hits": p.received(
    #         lambda a: a.classify_receiving(action_type=ActionType.PARRY)
    #         and a.classify_scoring(action_type=ActionType.PARRY)
    #     ),
    #     # "Renewal Hits": ,
    # },
}


def calculate_metrics(provider: FencerActionProvider) -> list[str]:
    """Calculate all metrics and return formatted strings."""
    results: list[str] = []

    # Add numerical metrics
    results.extend(
        format_metric(name, formula, provider) for name, formula in METRICS.items()
    )

    # Add distribution metrics
    results.extend(
        format_distribution(name, dist_fn, provider)
        for name, dist_fn in DISTRIBUTIONS.items()
    )

    return results


# def riposte_to_parry_ratio(p: FencerActionProvider) -> float:
#     """Calculates the ratio of successful ripostes to total parries."""
#     # isn't counter counter ripostes I think
#     return p.scored(Action.is_scoring_riposte) / (
#         p.scored(Action.is_scoring_riposte) + p.received(Action.is_failing_parry)
#     )
