from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

IntFunc = Callable[[], int]


@dataclass
class FencerActionProvider:
    attacks_scored: IntFunc
    attacks_received: IntFunc
    counter_attacks_scored: IntFunc
    counter_attacks_received: IntFunc
    ripostes_scored: IntFunc
    ripostes_received: IntFunc
    attacks_received_from_parries: IntFunc
    attacks_received_from_counter_attacks: IntFunc
    attacks_scored_from_parries: IntFunc
    attacks_scored_from_counter_attacks: IntFunc


class DataProvider(ABC):
    @abstractmethod
    def get_fencer_action_provider(self, fencer_name: str) -> FencerActionProvider: ...

    @abstractmethod
    def get_date_fencer_action_provider(
        self, date: str, fencer_name: str
    ) -> FencerActionProvider: ...

    @abstractmethod
    def get_bout_fencer_action_provider(
        self, date: str, fencer: str, opponent: str
    ) -> FencerActionProvider: ...
