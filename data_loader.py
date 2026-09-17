"""Handles reading the raw match-stats CSV and turning it into structured data.

This module has one job: get the data out of the CSV file and into a
usable, well-typed shape. It does not calculate ratings or print reports.
"""

import csv
from dataclasses import dataclass


@dataclass
class PlayerMatchStat:
    """A single player's stat line from a single match."""
    match_id: int
    match_date: str
    team: str
    opponent: str
    venue: str
    result: str
    player_name: str
    position: str
    minutes_played: int
    goals: int
    assists: int
    tackles_won: int
    saves: int
    passes_completed: int
    shots_on_target: int
    yellow_cards: int


def load_match_stats(filepath):
    """Reads the match-stats CSV file into a list of PlayerMatchStat records.

    Parameters:
        filepath (str): Path to the soccer_match_stats.csv file.

    Returns:
        list[PlayerMatchStat]: One record per player-match row in the file.
    """
    records = []
    with open(filepath, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records.append(_row_to_record(row))
    return records


def _row_to_record(row):
    """Converts a single raw CSV row (dict of strings) into a PlayerMatchStat."""
    return PlayerMatchStat(
        match_id=int(row["match_id"]),
        match_date=row["match_date"],
        team=row["team"],
        opponent=row["opponent"],
        venue=row["venue"],
        result=row["result"],
        player_name=row["player_name"],
        position=row["position"],
        minutes_played=int(row["minutes_played"]),
        goals=int(row["goals"]),
        assists=int(row["assists"]),
        tackles_won=int(row["tackles_won"]),
        saves=int(row["saves"]),
        passes_completed=int(row["passes_completed"]),
        shots_on_target=int(row["shots_on_target"]),
        yellow_cards=int(row["yellow_cards"]),
    )
