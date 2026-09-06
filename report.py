"""Builds reports and charts from a rated match-stats DataFrame.

This module has one job: summarize and visualize data that already has
an 'impact_rating' column. It does not load data or calculate ratings.
"""

import matplotlib
matplotlib.use("Agg")  # render to file, no GUI window needed
import matplotlib.pyplot as plt


def match_leaderboard(df, match_id):
    """Returns a match's players ranked by impact rating, highest first.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        match_id (int): The match to filter for. Must be a positive integer.

    Returns:
        pandas.DataFrame: Rows for that match, sorted by impact_rating descending.

    Raises:
        ValueError: If match_id is not a positive integer.
    """
    if match_id <= 0:
        raise ValueError(f"match_id must be positive (got {match_id}).")
    match_df = df[df["match_id"] == match_id]
    return match_df.sort_values("impact_rating", ascending=False)


def team_average_rating_by_position(df, team_name):
    """Averages impact rating by position for a given team, across all matches.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        team_name (str): The team to filter for. Must be non-empty.

    Returns:
        pandas.Series: Average impact_rating indexed by position.

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    team_df = df[df["team"] == team_name]
    return team_df.groupby("position")["impact_rating"].mean().sort_values(ascending=False)


def plot_top_performers(df, team_name, top_n, output_path):
    """Saves a bar chart of a team's top-N players by average impact rating.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        team_name (str): The team to chart. Must be non-empty.
        top_n (int): How many players to show. Must be a positive integer.
        output_path (str): Where to save the chart image.

    Raises:
        ValueError: If team_name is empty or top_n is not positive.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    if top_n <= 0:
        raise ValueError(f"top_n must be positive (got {top_n}).")

    team_df = df[df["team"] == team_name]
    avg_by_player = (
        team_df.groupby("player_name")["impact_rating"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    avg_by_player.plot(
        kind="bar",
        title=f"{team_name}: Top {top_n} Players by Avg. Impact Rating",
        ylabel="Avg. Impact Rating (0-10)",
        xlabel="Player",
        legend=False,
    )
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
