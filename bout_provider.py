from typing import List
from bout import Bout
from models import BoutData


def get_bouts(bout_data_list: List[BoutData]) -> List[Bout]:
    """
    Creates a list of Bout objects from a list of BoutData objects.

    Args:
        bout_data_list: A list of BoutData objects.

    Returns:
        A list of Bout objects.
    """
    return [Bout(bout_data) for bout_data in bout_data_list]
