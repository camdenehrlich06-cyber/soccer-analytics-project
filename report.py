"""Builds reports and charts from a list of rated PlayerMatchStat records.

This module has one job: summarize and visualize the stat data. It does
not load data or calculate ratings itself.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ratings import rate_player_stat


def filter_by_match(stats, match_id):
    """Returns only the stat lines belonging to a given match.

    Raises:
        ValueError: If match_id is not a positive integer.
    """
    if match_id <= 0:
        raise ValueError(f"match_id must be positive (got {match_id}).")
    return [s for s in stats if s.match_id == match_id]


def filter_by_team(stats, team_name):
    """Returns only the stat lines belonging to a given team, across all matches.

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    return [s for s in stats if s.team == team_name]


def rank_by_rating(stats, descending=True):
    """Sorts stat lines into a leaderboard by impact rating (custom key)."""
    return sorted(stats, key=rate_player_stat, reverse=descending)


def rank_by_goal_contributions(stats):
    """Sorts stat lines by goals first, using assists to break ties."""
    return sorted(stats, key=lambda s: (s.goals, s.assists), reverse=True)


def team_average_rating_by_position(stats, team_name):
    """Averages impact rating by position for a given team, across all matches.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        team_name (str): The team to filter for. Must be non-empty.

    Returns:
        dict[str, float]: Average impact rating per position, sorted highest first.

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    team_stats = filter_by_team(stats, team_name)

    totals = {}
    for stat in team_stats:
        totals.setdefault(stat.position, []).append(rate_player_stat(stat))

    averages = {pos: round(sum(ratings) / len(ratings), 2) for pos, ratings in totals.items()}
    return dict(sorted(averages.items(), key=lambda item: item[1], reverse=True))


def player_form(stats, player_name, window=3):
    """Tracks a player's rolling average impact rating over their last N matches.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        player_name (str): The player to track. Must be non-empty.
        window (int): Number of most recent matches to average. Must be positive.

    Returns:
        list[tuple]: (match_date, opponent, impact_rating, form_rating) per match,
            in date order.

    Raises:
        ValueError: If player_name is empty or window is not positive.
    """
    if not player_name:
        raise ValueError("player_name cannot be empty.")
    if window <= 0:
        raise ValueError(f"window must be positive (got {window}).")

    player_stats = sorted(
        [s for s in stats if s.player_name == player_name],
        key=lambda s: s.match_date,
    )

    results = []
    recent_ratings = []
    for stat in player_stats:
        rating = rate_player_stat(stat)
        recent_ratings.append(rating)
        if len(recent_ratings) > window:
            recent_ratings.pop(0)
        form_rating = round(sum(recent_ratings) / len(recent_ratings), 2)
        results.append((stat.match_date, stat.opponent, rating, form_rating))
    return results


def home_away_split(stats, team_name):
    """Compares a team's average impact rating at home vs. away.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        team_name (str): The team to compare. Must be non-empty.

    Returns:
        dict[str, float]: Average impact rating keyed by 'Home' / 'Away'.

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    team_stats = filter_by_team(stats, team_name)

    totals = {"Home": [], "Away": []}
    for stat in team_stats:
        totals[stat.venue].append(rate_player_stat(stat))

    return {venue: round(sum(ratings) / len(ratings), 2) for venue, ratings in totals.items() if ratings}


def _pearson_correlation(xs, ys):
    """Computes the Pearson correlation coefficient between two equal-length lists."""
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denom_x = sum((x - mean_x) ** 2 for x in xs) ** 0.5
    denom_y = sum((y - mean_y) ** 2 for y in ys) ** 0.5
    if denom_x == 0 or denom_y == 0:
        return 0.0
    return numerator / (denom_x * denom_y)


def stat_correlations_with_rating(stats, stat_names):
    """Checks how strongly each given stat correlates with impact rating.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        stat_names (list[str]): Attribute names on PlayerMatchStat to check
            (e.g. "goals", "tackles_won").

    Returns:
        list[tuple]: (stat_name, correlation) pairs, sorted highest first.

    Raises:
        ValueError: If stat_names is empty.
    """
    if not stat_names:
        raise ValueError("stat_names cannot be empty.")

    ratings = [rate_player_stat(s) for s in stats]
    results = []
    for name in stat_names:
        values = [getattr(s, name) for s in stats]
        results.append((name, round(_pearson_correlation(values, ratings), 3)))
    return sorted(results, key=lambda item: item[1], reverse=True)


def build_report_lines(stats, title):
    """Builds the text lines of a report for a given set of stat lines."""
    lines = [f"=== {title} ==="]
    for rank, stat in enumerate(stats, start=1):
        rating = rate_player_stat(stat)
        lines.append(
            f"{rank:>2}. {stat.player_name:<20} {stat.position:<3} {stat.team:<15} "
            f"G:{stat.goals} A:{stat.assists} T:{stat.tackles_won} "
            f"S:{stat.saves} Min:{stat.minutes_played:<3} -> Rating: {rating}"
        )
    return lines


def print_report(stats, title):
    """Prints a report for the given stat lines directly to the screen."""
    for line in build_report_lines(stats, title):
        print(line)


def save_report(stats, title, filepath):
    """Writes a report for the given stat lines out to a text file."""
    lines = build_report_lines(stats, title)
    with open(filepath, "w") as out_file:
        out_file.write("\n".join(lines) + "\n")


def plot_top_performers(stats, team_name, top_n, output_path):
    """Saves a bar chart of a team's top-N players by average impact rating.

    Raises:
        ValueError: If team_name is empty or top_n is not positive.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    if top_n <= 0:
        raise ValueError(f"top_n must be positive (got {top_n}).")

    team_stats = filter_by_team(stats, team_name)
    totals = {}
    for stat in team_stats:
        totals.setdefault(stat.player_name, []).append(rate_player_stat(stat))
    averages = {name: sum(r) / len(r) for name, r in totals.items()}
    top_players = sorted(averages.items(), key=lambda item: item[1], reverse=True)[:top_n]

    names = [p[0] for p in top_players]
    values = [p[1] for p in top_players]

    plt.figure()
    plt.bar(names, values)
    plt.title(f"{team_name}: Top {top_n} Players by Avg. Impact Rating")
    plt.ylabel("Avg. Impact Rating (0-10)")
    plt.xlabel("Player")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_player_form(stats, player_name, window, output_path):
    """Saves a line chart of a player's rating and rolling form over time.

    Raises:
        ValueError: If player_name is empty.
    """
    if not player_name:
        raise ValueError("player_name cannot be empty.")

    form_data = player_form(stats, player_name, window)
    dates = [row[0] for row in form_data]
    ratings = [row[2] for row in form_data]
    form_ratings = [row[3] for row in form_data]

    plt.figure()
    plt.plot(dates, ratings, marker="o", label="Impact Rating")
    plt.plot(dates, form_ratings, marker="o", label=f"{window}-Match Form")
    plt.title(f"{player_name}: Impact Rating vs. {window}-Match Form")
    plt.ylabel("Impact Rating (0-10)")
    plt.xlabel("Match Date")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
