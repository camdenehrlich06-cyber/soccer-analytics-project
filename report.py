"""Builds reports and charts from a rated match-stats DataFrame.

This module has one job: summarize and visualize data that already has
an 'impact_rating' column. It does not load data or calculate ratings.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def match_leaderboard(df, match_id):
    """Returns a match's players ranked by impact rating, highest first.

    Raises:
        ValueError: If match_id is not a positive integer.
    """
    if match_id <= 0:
        raise ValueError(f"match_id must be positive (got {match_id}).")
    match_df = df[df["match_id"] == match_id]
    return match_df.sort_values("impact_rating", ascending=False)


def team_average_rating_by_position(df, team_name):
    """Averages impact rating by position for a given team, across all matches.

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    team_df = df[df["team"] == team_name]
    return team_df.groupby("position")["impact_rating"].mean().sort_values(ascending=False)


def player_form(df, player_name, window=3):
    """Tracks a player's rolling average impact rating over their last N matches.

    This answers "who is trending up or down right now?" rather than just
    "who has the best season average?" -- a player can have a strong overall
    average while their most recent matches are declining, or vice versa.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        player_name (str): The player to track. Must be non-empty.
        window (int): Number of most recent matches to average. Must be positive.

    Returns:
        pandas.DataFrame: That player's matches in date order, with a
            'form_rating' column showing the rolling average.

    Raises:
        ValueError: If player_name is empty or window is not positive.
    """
    if not player_name:
        raise ValueError("player_name cannot be empty.")
    if window <= 0:
        raise ValueError(f"window must be positive (got {window}).")

    player_df = df[df["player_name"] == player_name].sort_values("match_date").copy()
    player_df["form_rating"] = player_df["impact_rating"].rolling(window, min_periods=1).mean().round(2)
    return player_df[["match_date", "opponent", "impact_rating", "form_rating"]]


def home_away_split(df, team_name):
    """Compares a team's average impact rating at home vs. away.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        team_name (str): The team to compare. Must be non-empty.

    Returns:
        pandas.Series: Average impact_rating indexed by venue ('Home'/'Away').

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    team_df = df[df["team"] == team_name]
    return team_df.groupby("venue")["impact_rating"].mean().round(2)


def stat_correlations_with_rating(df, stat_columns):
    """Checks how strongly each given stat correlates with impact rating.

    Useful for sanity-checking the rating formula itself: if a stat that
    should matter (e.g. goals) shows near-zero correlation, that's worth
    investigating before trusting the rating.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        stat_columns (list[str]): Column names to correlate against impact_rating.

    Returns:
        pandas.Series: Correlation coefficient per stat, sorted descending.

    Raises:
        ValueError: If stat_columns is empty.
    """
    if not stat_columns:
        raise ValueError("stat_columns cannot be empty.")
    return df[stat_columns + ["impact_rating"]].corr()["impact_rating"].drop("impact_rating").sort_values(ascending=False)


def plot_top_performers(df, team_name, top_n, output_path):
    """Saves a bar chart of a team's top-N players by average impact rating.

    Raises:
        ValueError: If team_name is empty or top_n is not positive.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    if top_n <= 0:
        raise ValueError(f"top_n must be positive (got {top_n}).")

    team_df = df[df["team"] == team_name]
    avg_by_player = (
        team_df.groupby("player_name")["impact_rating"].mean()
        .sort_values(ascending=False).head(top_n)
    )
    avg_by_player.plot(
        kind="bar", title=f"{team_name}: Top {top_n} Players by Avg. Impact Rating",
        ylabel="Avg. Impact Rating (0-10)", xlabel="Player", legend=False,
    )
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_player_form(df, player_name, window, output_path):
    """Saves a line chart of a player's rating and rolling form over time.

    Parameters:
        df (pandas.DataFrame): Rated match-stats data.
        player_name (str): The player to chart. Must be non-empty.
        window (int): Rolling window size for the form line.
        output_path (str): Where to save the chart image.

    Raises:
        ValueError: If player_name is empty.
    """
    if not player_name:
        raise ValueError("player_name cannot be empty.")

    form_df = player_form(df, player_name, window).set_index("match_date")
    form_df[["impact_rating", "form_rating"]].plot(
        kind="line", marker="o",
        title=f"{player_name}: Impact Rating vs. {window}-Match Form",
        ylabel="Impact Rating (0-10)", xlabel="Match Date",
    )
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
