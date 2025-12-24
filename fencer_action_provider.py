from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable, List, Tuple

from actions import Action


class FencerActionProvider(ABC):
    @abstractmethod
    def scored(self, action_filter: Callable[[Action], bool]) -> int: ...

    @abstractmethod
    def received(self, action_filter: Callable[[Action], bool]) -> int: ...


class ActionOutcome(Enum):
    FOR = auto()
    AGAINST = auto()


class OrderedFencerActionProvider(FencerActionProvider):
    @abstractmethod
    def get_actions(
        self,
    ) -> List[Tuple[Tuple[Action, ActionOutcome], Tuple[Action, ActionOutcome]]]: ...
