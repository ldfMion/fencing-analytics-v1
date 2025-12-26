from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

from actions import Action
from models import ActionOutcome, BoutData


class FencerActionProvider(ABC):
    @abstractmethod
    def scored(self, action_filter: Callable[[Action], bool]) -> int: ...

    @abstractmethod
    def received(self, action_filter: Callable[[Action], bool]) -> int: ...


class OrderedFencerActionProvider(FencerActionProvider):
    @abstractmethod
    def get_actions(
        self,
    ) -> List[Tuple[Tuple[Action, ActionOutcome], Tuple[Action, ActionOutcome]]]: ...


class BoutFencerActionProvider(FencerActionProvider):
    def __init__(self, fencer_name: str, bout_data: BoutData):
        self._fencer_name = fencer_name
        self._bout_data = bout_data

    def scored(self, action_filter: Callable[[Action], bool]) -> int:
        count = 0
        for touch in self._bout_data.touches:
            if action_filter(touch.action):
                if (
                    touch.side == "L"
                    and self._fencer_name == self._bout_data.left_fencer
                ) or (
                    touch.side == "R"
                    and self._fencer_name == self._bout_data.right_fencer
                ):
                    count += 1
        return count

    def received(self, action_filter: Callable[[Action], bool]) -> int:
        count = 0
        for touch in self._bout_data.touches:
            if action_filter(touch.action):
                if (
                    touch.side == "L"
                    and self._fencer_name == self._bout_data.right_fencer
                ) or (
                    touch.side == "R"
                    and self._fencer_name == self._bout_data.left_fencer
                ):
                    count += 1
        return count
