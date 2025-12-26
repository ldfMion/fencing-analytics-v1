from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from actions import Action


@dataclass
class Touch:
    """
    Represents a single touch in a bout.
    """

    action: Action
    side: str
    left_score: int
    right_score: int


@dataclass
class BoutData:
    """
    Represents the data for a single fencing bout.
    """

    left_fencer: str
    right_fencer: str
    date: str
    touches: List[Touch]


class ActionOutcome(Enum):
    FOR = auto()
    AGAINST = auto()
