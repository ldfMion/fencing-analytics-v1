from dataclasses import dataclass
from enum import Enum, auto


class ActionType(Enum):
    ATTACK = "A"
    COUNTER_ATTACK = "C"
    PARRY = "P"
    RIPOSTE = "R"
    PREP = "Ap"
    ATTACK_RENEWAL = "Ar"
    RENEWAL = "r"


@dataclass
class Action:
    action: str
    response: str | None

    def _has_type(self, action_str: str | None, action_type: ActionType) -> bool:
        if action_str is None:
            return False
        return action_type.value in action_str

    def is_scoring_attack(self) -> bool:
        return self._has_type(self.action, ActionType.ATTACK)

    def is_scoring_counter_attack(self) -> bool:
        return self._has_type(self.action, ActionType.COUNTER_ATTACK)

    def is_scoring_riposte(self) -> bool:
        return self._has_type(self.action, ActionType.RIPOSTE)

    def is_failing_attack(self) -> bool:
        return (
            self.is_scoring_counter_attack()
            or self.is_scoring_riposte()
            or self.is_simultaneous_attack()
            or self.is_attack_on_prep()
        )

    def is_simultaneous_attack(self) -> bool:
        return self.is_scoring_attack() and self._has_type(
            self.response, ActionType.ATTACK
        )

    def is_attack_on_prep(self) -> bool:
        return self._has_type(self.action, ActionType.PREP)

    def is_scoring_defense(self) -> bool:
        return self.is_scoring_counter_attack() or self.is_scoring_riposte()

    def is_failing_defense(self) -> bool:
        return self.is_scoring_attack() and (
            self.is_failing_counter_attack() or self.is_failing_parry()
        )

    def is_failing_counter_attack(self) -> bool:
        return self._has_type(self.response, ActionType.COUNTER_ATTACK)

    def is_failing_parry(self) -> bool:
        return self._has_type(self.action, ActionType.ATTACK_RENEWAL) or self._has_type(
            self.response, ActionType.PARRY
        )

    def is_scoring_priority(self) -> bool:
        return not (
            self.is_scoring_counter_attack()
            or self._has_type(self.action, ActionType.RENEWAL)
        )

    def is_failing_priority(self) -> bool:
        if self.is_failing_counter_attack():
            return False
        if self.response is not None:
            return not self._has_type(self.response, ActionType.RENEWAL)
        return True
