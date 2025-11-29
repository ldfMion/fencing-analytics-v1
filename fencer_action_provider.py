from abc import ABC, abstractmethod
from typing import Callable

IntFunc = Callable[[], int]


class FencerActionProvider(ABC):
    def __init__(self, fencer_name: str):
        self._fencer_name = fencer_name

    @abstractmethod
    def attacks_scored(self) -> int: ...

    @abstractmethod
    def attacks_received(self) -> int: ...

    @abstractmethod
    def counter_attacks_scored(self) -> int: ...

    @abstractmethod
    def counter_attacks_received(self) -> int: ...

    @abstractmethod
    def ripostes_scored(self) -> int: ...

    @abstractmethod
    def ripostes_received(self) -> int: ...

    @abstractmethod
    def attacks_received_from_parries(self) -> int: ...

    @abstractmethod
    def attacks_received_from_counter_attacks(self) -> int: ...

    @abstractmethod
    def attacks_scored_from_parries(self) -> int: ...

    @abstractmethod
    def attacks_scored_from_counter_attacks(self) -> int: ...
