"""Calculates player performance impact ratings.

This module has one job: turn raw match stats into an impact rating.
It knows nothing about CSV files or how results get printed.
"""

POSITION_WEIGHTS = {
    "GK": {"goals": 4.0, "assists": 3.0, "tackles_won": 1.0, "saves": 3.0},
    "DF": {"goals": 4.0, "assists": 3.0, "tackles_won": 2.5, "saves": 0.0},
    "MF": {"goals": 3.5, "assists": 3.5, "tackles_won": 1.5, "saves": 0.0},
    "FW": {"goals": 5.0, "assists": 3.0, "tackles_won": 0.5, "saves": 0.0},
}

MAX_RATING = 10.0


def calculate_impact_rating(goals, assists, tackles_won, minutes_played, saves, position):
    """Calculates a soccer player's performance impact rating per 90 minutes.

    Parameters:
        goals (int): Total goals scored in the match.
        assists (int): Total assists provided in the match.
        tackles_won (int): Total successful defensive tackles.
        minutes_played (int): Number of minutes played on the pitch.
        saves (int): Number of saves made in the match (0 for outfield players).
        position (str): The player's position: "GK", "DF", "MF", or "FW".

    Returns:
        float: A calculated impact score normalized on a scale from 0.0 to 10.0.

    Raises:
        ValueError: If any stat is negative, minutes_played exceeds 120,
            or position is not a recognized code.
    """
    _check_impact_rating_preconditions(goals, assists, tackles_won, minutes_played, saves, position)

    weights = POSITION_WEIGHTS[position]
    raw_score = (
        goals * weights["goals"]
        + assists * weights["assists"]
        + tackles_won * weights["tackles_won"]
        + saves * weights["saves"]
    )

    if minutes_played == 0:
        return 0.0

    per_90_score = raw_score * (90 / minutes_played)
    return round(min(per_90_score, MAX_RATING), 2)


def _check_impact_rating_preconditions(goals, assists, tackles_won, minutes_played, saves, position):
    """Validates inputs before a rating is calculated.

    Raises:
        ValueError: If any precondition is violated.
    """
    stat_values = {
        "goals": goals, "assists": assists, "tackles_won": tackles_won,
        "minutes_played": minutes_played, "saves": saves,
    }
    for name, value in stat_values.items():
        if value < 0:
            raise ValueError(f"{name} cannot be negative (got {value}).")
    if minutes_played > 120:
        raise ValueError(f"minutes_played cannot exceed 120 (got {minutes_played}).")
    if position not in POSITION_WEIGHTS:
        valid = ", ".join(POSITION_WEIGHTS)
        raise ValueError(f"position must be one of [{valid}] (got {position!r}).")


def add_impact_rating_column(df):
    """Adds an 'impact_rating' column to a match-stats DataFrame.

    Applies calculate_impact_rating() row by row so the exact same,
    already-validated formula used elsewhere in this project is reused
    here rather than reimplemented in pandas-specific vector math.

    Parameters:
        df (pandas.DataFrame): Must contain goals, assists, tackles_won,
            minutes_played, saves, and position columns.

    Returns:
        pandas.DataFrame: A copy of df with an added 'impact_rating' column.
    """
    df = df.copy()
    df["impact_rating"] = df.apply(
        lambda row: calculate_impact_rating(
            goals=row["goals"], assists=row["assists"], tackles_won=row["tackles_won"],
            minutes_played=row["minutes_played"], saves=row["saves"], position=row["position"],
        ),
        axis=1,
    )
    return df
