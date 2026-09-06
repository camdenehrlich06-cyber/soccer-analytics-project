"""Handles reading the raw match-stats CSV into a pandas DataFrame.

This module has one job: get the data out of the CSV file and into a
DataFrame with the right column types. It does not calculate ratings
or print reports.
"""

import pandas as pd

INT_COLUMNS = [
    "match_id", "minutes_played", "goals", "assists",
    "tackles_won", "saves", "passes_completed", "shots_on_target", "yellow_cards",
]


def load_match_stats(filepath):
    """Reads the match-stats CSV file into a pandas DataFrame.

    Parameters:
        filepath (str): Path to the soccer_match_stats.csv file.

    Returns:
        pandas.DataFrame: One row per player-match stat line, with
            match_date parsed as a datetime and numeric columns cast to int.
    """
    df = pd.read_csv(filepath)
    df["match_date"] = pd.to_datetime(df["match_date"])
    df[INT_COLUMNS] = df[INT_COLUMNS].astype(int)
    return df
