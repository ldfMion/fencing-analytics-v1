from dataclasses import dataclass
from enum import Enum


class TacticalIntent(Enum):
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"


class ActionType(Enum):
    ATTACK = "A"
    COUNTER_ATTACK = "C"
    PARRY = "P"


class Priority(Enum):
    WITH_PRIORITY = "with_priority"
    WITHOUT_PRIORITY = "without_priority"


class DefensiveAlternative(Enum):
    PARRY = "parry"
    COUNTER_ATTACK = "counter_attack"
    ATTACK_ON_PREP = "attack_on_prep"
    DEFENSE_WITH_DISTANCE = "defense_with_distance"


all_actions = {
    # attacks
    "Aan": {
        "name": "Answering attack",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": DefensiveAlternative.DEFENSE_WITH_DISTANCE,
        },
    },
    "Abt": {
        "name": "Broken time attack",
        "classifications": {
            "tactical_intent": TacticalIntent.OFFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": None,
        },
    },
    "Act": {
        "name": "Attack with counter time",
        "classifications": {
            "tactical_intent": TacticalIntent.OFFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": None,
        },
    },
    "Af": {
        "name": "Fleche attack",
        "classifications": {
            "tactical_intent": TacticalIntent.OFFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": None,
        },
    },
    "Ap": {
        "name": "Attack on preparation",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": DefensiveAlternative.ATTACK_ON_PREP,
        },
    },
    "Ar": {
        "name": "Attack renewal",
        "classifications": {
            "tactical_intent": TacticalIntent.OFFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITHOUT_PRIORITY,
            "defensive_alternative": None,
        },
    },
    # counter attacks
    "Cc": {
        "name": "Closing counter attack",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.COUNTER_ATTACK,
            "priority": Priority.WITHOUT_PRIORITY,
            "defensive_alternative": DefensiveAlternative.COUNTER_ATTACK,
        },
    },
    "Cr": {
        "name": "Counter attack renewal",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.COUNTER_ATTACK,
            "priority": Priority.WITHOUT_PRIORITY,
            "defensive_alternative": DefensiveAlternative.COUNTER_ATTACK,
        },
    },
    "Csh": {
        "name": "Counter attack stop hit",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.COUNTER_ATTACK,
            "priority": Priority.WITHOUT_PRIORITY,
            "defensive_alternative": DefensiveAlternative.COUNTER_ATTACK,
        },
    },
    "Cd": {
        "name": "Ducking counter attack",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.COUNTER_ATTACK,
            "priority": Priority.WITHOUT_PRIORITY,
            "defensive_alternative": DefensiveAlternative.COUNTER_ATTACK,
        },
    },
    # this is probably not a good design decision but this has to be last otherwise the substring
    # search for attacks will always match this without checking the others
    "A": {
        "name": "Attack",
        "classifications": {
            "tactical_intent": TacticalIntent.OFFENSIVE,
            "action_type": ActionType.ATTACK,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": None,
        },
    },
    # ripostes
    "R": {
        "name": "Riposte",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.PARRY,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": DefensiveAlternative.PARRY,
        },
    },
    "Rr": {
        "name": "Riposte renewal",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.PARRY,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": DefensiveAlternative.PARRY,
        },
    },
    "cR": {
        "name": "Counter riposte",
        "classifications": {
            "tactical_intent": TacticalIntent.DEFENSIVE,
            "action_type": ActionType.PARRY,
            "priority": Priority.WITH_PRIORITY,
            "defensive_alternative": DefensiveAlternative.PARRY,
        },
    },
}

all_responses = {
    "A": {
        "name": "Failed attack",
        "classifications": {
            "tactical_intent": TacticalIntent.OFFENSIVE,
            "action_type": ActionType.ATTACK,
            "defensive_alternative": None,
        },
    },
    "Ap": {
        "name": "Failed attack on preparation",
        "classifications": {
            "action_type": ActionType.ATTACK,
            "defensive_alternative": DefensiveAlternative.ATTACK_ON_PREP,
        },
    },
    "Ar": {
        "name": "Failed attack renewal",
        "classifications": {
            "action_type": ActionType.ATTACK,
            "defensive_alternative": None,
        },
    },
    "Cc": {
        "name": "Failed closing counter attack",
        "classifications": {
            "action_type": ActionType.COUNTER_ATTACK,
            "defensive_alternative": None,
        },
    },
    "Cd": {
        "name": "Failed ducking counter attack",
        "classifications": {
            "action_type": ActionType.COUNTER_ATTACK,
            "defensive_alternative": DefensiveAlternative.COUNTER_ATTACK,
        },
    },
    "Csh": {
        "name": "Failed counter attack stop hit",
        "classifications": {
            "action_type": ActionType.COUNTER_ATTACK,
            "defensive_alternative": DefensiveAlternative.COUNTER_ATTACK,
        },
    },
    "D": {
        "name": "Failed defense with distance",
        "classifications": {
            "action_type": ActionType.ATTACK,  # this is because this corresponds to an answering attack if it were successful, but I don't know if that's a good idea
            "defensive_alternative": DefensiveAlternative.DEFENSE_WITH_DISTANCE,
        },
    },
    "P": {
        "name": "Failed parry",
        "classifications": {
            "action_type": ActionType.PARRY,
            "defensive_alternative": DefensiveAlternative.PARRY,
        },
    },
    "Rr": {
        "name": "Failed riposte remise",
        "classifications": {
            "action_type": ActionType.PARRY,
            "defensive_alternative": DefensiveAlternative.PARRY,
        },
    },
}

all_actions_strings = list(all_actions.keys())
all_responses_strings = list(all_responses.keys())


@dataclass
class Action:
    action: str
    response: str | None

    def __init__(self, action: str, response: str | None):
        self.action = action
        assert action != ""
        assert response != ""
        assert str(response) != "nan"
        self.response = response

    # --- scoring perspective ---

    def scoring_tactical_intent_is(self, tactical_intent: TacticalIntent):
        found_action = self._find_action()
        return (
            all_actions[found_action]["classifications"]["tactical_intent"]
            == tactical_intent
        )

    def scoring_action_type_is(self, action_type: ActionType):
        found_action = self._find_action()
        return (
            all_actions[found_action]["classifications"]["action_type"] == action_type
        )

    def scoring_priority_is(self, priority: Priority):
        found_action = self._find_action()
        return all_actions[found_action]["classifications"]["priority"] == priority

    def scoring_defensive_alternative_is(
        self, defensive_alternative: DefensiveAlternative
    ):
        found_action = self._find_action()
        return (
            all_actions[found_action]["classifications"]["defensive_alternative"]
            == defensive_alternative
        )

    # --- receiving perspective ---

    def receiving_tactical_intent_is(self, tactical_intent: TacticalIntent):
        found_response = self._find_response()
        if (
            found_response is None
            or "tactical_intent" not in all_responses[found_response]["classifications"]
        ):
            found_action = self._find_action()
            # if the response is empty, then the tactical intent classification from the receiving perspective
            # is the opposite of the one from the scoring perspective
            action_tactical_intent = all_actions[found_action]["classifications"][
                "tactical_intent"
            ]
            return action_tactical_intent != tactical_intent
        else:
            response_tactical_intent = all_responses[found_response]["classifications"][
                "tactical_intent"
            ]
            return response_tactical_intent == tactical_intent

    def receiving_action_type_is(self, action_type: ActionType):
        found_response = self._find_response()
        if found_response is None:
            found_action = self._find_action()
            # action special cases
            if found_action == "Ar":
                # if the action is an attack renewal, then the response is a parry
                # so we exclude it if we aren't looking for parries
                return action_type == ActionType.PARRY
            if found_action == "Ap":
                # if the action is an attack on prep with an empty response we'll assume the opponent was attacking
                # so we exclude it if we aren't looking for attacks
                return action_type == ActionType.ATTACK
            action_action_type = all_actions[found_action]["classifications"][
                "action_type"
            ]
            if action_action_type == ActionType.ATTACK:
                raise ValueError(
                    f"To have an action_type from the receiving perspective for a scoring attack (not Ar), the response must be present. Action: '{self}'"
                )
            else:
                # then the action is a counter attack or parry, so the ActionType of the response is attack
                # so we need to exclude it if we aren't looking for an attack
                return action_type == ActionType.ATTACK
        else:
            response_action_type = all_responses[found_response]["classifications"][
                "action_type"
            ]
            return action_type == response_action_type

    def receiving_priority_is(self, priority: Priority):
        return not self.scoring_priority_is(priority)

    def receiving_defensive_alternative_is(
        self, defensive_alternative: DefensiveAlternative
    ):
        found_response = self._find_response()
        if found_response is None:
            found_action = self._find_action()
            if found_action == "Ar":
                return defensive_alternative == DefensiveAlternative.PARRY
            if found_action == "Ap":
                return defensive_alternative == DefensiveAlternative.ATTACK_ON_PREP
            raise ValueError(
                f"Filtering for defensive alternative in a receiving action that doesn't have a defined response. Action: {self}"
            )
        response_defensive_alternative = all_responses[found_response][
            "classifications"
        ]["defensive_alternative"]
        return response_defensive_alternative == defensive_alternative

    def _find_action(self):
        # find the first action in the dict that has self.action as a substring
        found_action = next(
            (string for string in all_actions_strings if string in self.action), None
        )
        if found_action is None:
            raise ValueError(f"Invalid action: '{self.action}'")
        return found_action

    def _find_response(self):
        # find the first response in the dict that has self.response as a substring
        if self.response is None:
            return None
        found_response = next(
            (string for string in all_responses_strings if string in self.response),
            None,
        )
        if found_response is None:
            raise ValueError(f"Invalid response: {self.response}")
        return found_response
