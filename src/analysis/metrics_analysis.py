from multiprocessing import BoundedSemaphore
from typing import List, Tuple

import pandas as pd

from config import BOUTS_FILENAME, TOUCHES_FILENAME
from src.analysis.metrics import calculate_metrics
from src.analysis.metrics_report import create_bout_metrics_report
from src.data.constants import DATE
from src.data.csv_fencer_action_provider import CsvFencerActionProvider
from src.data.data_loader import load_data
from src.domain.bout import Bout
from src.domain.models import DataSources


def analyze_fencer(fencer_name: str, date: str | None, bout_type: str | None):
    """
    Performs analysis on a fencer's performance.

    Args:
        main_df: The main DataFrame containing all bout data.
        fencer_name: The name of the fencer to analyze.
    """
    sources = DataSources(touches_file=TOUCHES_FILENAME, bouts_file=BOUTS_FILENAME)
    data = load_data(sources.touches_file, sources.bouts_file)
    provider = CsvFencerActionProvider(
        fencer_name, data, date=date, bout_type=bout_type
    )
    metrics = calculate_metrics(provider)
    print("------- Analysis --------")
    for metric in metrics:
        print(metric)
    print()

    # bout_data_list = load_bouts_from_df(main_df)
    # bouts = get_bouts(bout_data_list)
    # analyze_bouts(bouts, fencer_name)


def analyze_bouts(bouts: List[Bout], fencer_name: str):
    """
    Performs analysis on a list of bouts.

    Args:
        bouts: A list of Bout objects.
        fencer_name: The name of the fencer to analyze.
    """
    print("Analyzing bouts: ")
    for bout in bouts:
        print(bout.get_summary())
        result = create_bout_metrics_report(bout._bout_data, fencer_name)
        for metric in result:
            print(metric)
        print()
