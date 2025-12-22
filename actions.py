ATTACK = "A"
COUNTER_ATTACK = "C"
PARRY = "P"
RIPOSTE = "R"


def is_attack(action: str):
    return ATTACK in action


def is_counter_attack(action: str):
    return COUNTER_ATTACK in action


def is_riposte(action: str):
    return RIPOSTE in action


def is_parry(response: str):
    return PARRY in response
