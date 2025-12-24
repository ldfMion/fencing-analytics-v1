from dataclasses import dataclass

ATTACK = "A"
COUNTER_ATTACK = "C"
PARRY = "P"
RIPOSTE = "R"
PREP = "Ap"

ATTACK_RENEWAL = "Ar"


@dataclass
class Action:
    action: str
    response: str | None

    def is_scoring_attack(self):
        return is_attack(self.action)

    def is_scoring_counter_attack(self):
        return is_counter_attack(self.action)

    def is_scoring_riposte(self):
        return is_riposte(self.action)

    def is_failing_attack(self):
        return (
            self.is_scoring_counter_attack()
            or self.is_scoring_riposte()
            or self.is_simultaneous_attack()
            or self.is_attack_on_prep()
        )

    def is_simultaneous_attack(self):
        return (
            is_attack(self.action)
            and (self.response is not None)
            and is_attack(self.response)
        )

    def is_attack_on_prep(self):
        return is_prep(self.action)

    def is_scoring_defense(self):
        return self.is_scoring_counter_attack() or self.is_scoring_riposte()

    def is_failing_defense(self):
        return self.is_scoring_attack() and (
            self.is_failing_counter_attack() or self.is_failing_parry()
        )

    def is_failing_counter_attack(self):
        if self.response is None:
            return False
        return is_counter_attack(self.response)

    def is_failing_parry(self):
        if is_attack_renewal(self.action):
            return True
        if self.response is None:
            return False
        return is_parry(self.response)


def is_attack(action: str):
    return ATTACK in action


def is_counter_attack(action: str):
    return COUNTER_ATTACK in action


def is_riposte(action: str):
    return RIPOSTE in action


def is_parry(response: str):
    return PARRY in response


def is_prep(action: str):
    return PREP in action


def is_attack_renewal(action: str):
    return ATTACK_RENEWAL in action
