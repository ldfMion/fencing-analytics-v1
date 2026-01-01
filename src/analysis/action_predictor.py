from enum import Enum, auto

from src.data.fencer_action_provider import OrderedFencerActionProvider
from src.domain.actions import Action
from src.domain.models import ActionOutcome


class ActionType(Enum):
    PARRY = auto()
    ATTACK = auto()
    COUNTER_ATTACK = auto()


class FencingActionPredictor:
    def __init__(
        self,
        provider: OrderedFencerActionProvider,
        alpha: float = 1.0,
    ) -> None:
        # We store: counts[(last_action, outcome)][next_action]
        self.counts = {
            (ActionType.ATTACK, ActionOutcome.FOR): {
                ActionType.PARRY: 0,
                ActionType.ATTACK: 0,
                ActionType.COUNTER_ATTACK: 0,
            },
            (ActionType.ATTACK, ActionOutcome.AGAINST): {
                ActionType.PARRY: 0,
                ActionType.ATTACK: 0,
                ActionType.COUNTER_ATTACK: 0,
            },
            (ActionType.PARRY, ActionOutcome.FOR): {
                ActionType.PARRY: 0,
                ActionType.ATTACK: 0,
                ActionType.COUNTER_ATTACK: 0,
            },
            (ActionType.PARRY, ActionOutcome.AGAINST): {
                ActionType.PARRY: 0,
                ActionType.ATTACK: 0,
                ActionType.COUNTER_ATTACK: 0,
            },
            (ActionType.COUNTER_ATTACK, ActionOutcome.FOR): {
                ActionType.PARRY: 0,
                ActionType.ATTACK: 0,
                ActionType.COUNTER_ATTACK: 0,
            },
            (ActionType.COUNTER_ATTACK, ActionOutcome.AGAINST): {
                ActionType.PARRY: 0,
                ActionType.ATTACK: 0,
                ActionType.COUNTER_ATTACK: 0,
            },
        }
        for (action, outcome), (next, next_outcome) in provider.get_actions():
            self.counts[
                (get_action_type(action, outcome == ActionOutcome.FOR), outcome)
            ][get_action_type(next, next_outcome == ActionOutcome.FOR)] += 1

    def predict(self, action: Action, outcome: ActionOutcome):
        """
        Given the raw data of the LAST touch, predict my NEXT action.
        """
        return self._predict(
            get_action_type(action, outcome == ActionOutcome.FOR), outcome
        )

    def _predict(self, action: ActionType, outcome: ActionOutcome):
        possibilities = self.counts[(action, outcome)]
        total_occurrences = sum(possibilities.values())

        if total_occurrences == 0:
            raise Exception(f"No historical data for this situation {action} {outcome}")

        # 3. Calculate percentages
        probs = {}
        for action, count in possibilities.items():
            probs[action] = round(count / total_occurrences, 2)

        return probs

    def show_probabilities(self):
        for action, outcome in {
            (ActionType.ATTACK, ActionOutcome.FOR),
            (ActionType.COUNTER_ATTACK, ActionOutcome.FOR),
            (ActionType.PARRY, ActionOutcome.FOR),
            (ActionType.ATTACK, ActionOutcome.AGAINST),
            (ActionType.COUNTER_ATTACK, ActionOutcome.AGAINST),
            (ActionType.PARRY, ActionOutcome.AGAINST),
        }:
            try:
                result = self._predict(action, outcome)
                print(f"{action}/{outcome}: {result}")
            except Exception as e:
                print(f"Error: {e}")


def get_action_type(action: Action, action_or_response: bool) -> ActionType:
    if action_or_response:
        if action.is_scoring_attack():
            return ActionType.ATTACK
        elif action.is_scoring_counter_attack():
            return ActionType.COUNTER_ATTACK
        elif action.is_scoring_riposte():
            return ActionType.PARRY
    else:
        if action.is_failing_attack():
            return ActionType.ATTACK
        elif action.is_failing_counter_attack():
            return ActionType.COUNTER_ATTACK
        elif action.is_failing_parry() or action.response == "D":
            return ActionType.PARRY
    raise Exception(f"Action {action} not classified {action_or_response}")
