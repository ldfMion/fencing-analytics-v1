from typing import List, Tuple

from src.domain.models import BoutData


class Bout:
    """
    Represents a single fencing bout between two fencers on a specific date.
    """

    def __init__(self, bout_data: BoutData):
        """
        Initializes a Bout object.

        Args:
            bout_data: The data for the bout.
        """
        self._bout_data = bout_data

    @property
    def left_fencer(self) -> str:
        return self._bout_data.left_fencer

    @property
    def right_fencer(self) -> str:
        return self._bout_data.right_fencer

    @property
    def date(self) -> str:
        return self._bout_data.date

    @property
    def bout_data(self) -> BoutData:
        return self._bout_data

    def get_summary(self) -> str:
        """
        Generates a string summary of the bout, showing the actions and responses.

        Returns:
            A formatted string with the bout's summary.
        """
        summary = f"{self.left_fencer} vs {self.right_fencer} ({self.date})---\n\n"
        for touch in self._bout_data.touches:
            action = touch.action.action
            response = touch.action.response
            if action:
                text = f"{action}"
                if response:
                    text += f" ({response})"
                if touch.side == "R":
                    pad = len(self.left_fencer) + 4 + len(text)
                    text = text.rjust(pad, " ")
                summary += text + "\n"
        return summary

    def score(self) -> Tuple[int, int]:
        """
        Returns the final score of the bout.

        Returns:
            A tuple containing the left fencer's score and the right fencer's score.
        """
        last_touch = self._bout_data.touches[-1]
        return (last_touch.left_score, last_touch.right_score)


def get_bouts(bout_data_list: List[BoutData]) -> List[Bout]:
    """
    Creates a list of Bout objects from a list of BoutData objects.

    Args:
        bout_data_list: A list of BoutData objects.

    Returns:
        A list of Bout objects.
    """
    return [Bout(bout_data) for bout_data in bout_data_list]
