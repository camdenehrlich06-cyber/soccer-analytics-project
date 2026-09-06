"""Builds and prints post-match, season, and leaderboard reports.

This module has one job: turn a list of PlayerMatchStat + rating pairs
into a readable report. It does not load data or calculate ratings itself.
"""

from ratings import rate_player_stat


def filter_by_match(stats, match_id):
    """Returns only the stat lines belonging to a given match.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        match_id (int): The match to filter for. Must be a positive integer.

    Returns:
        list[PlayerMatchStat]: Stat lines for that match only.

    Raises:
        ValueError: If match_id is not a positive integer.
    """
    if match_id <= 0:
        raise ValueError(f"match_id must be positive (got {match_id}).")
    return [s for s in stats if s.match_id == match_id]


def filter_by_team(stats, team_name):
    """Returns only the stat lines belonging to a given team, across all matches.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        team_name (str): The team to filter for. Must be non-empty.

    Returns:
        list[PlayerMatchStat]: Stat lines for that team only.

    Raises:
        ValueError: If team_name is empty.
    """
    if not team_name:
        raise ValueError("team_name cannot be empty.")
    return [s for s in stats if s.team == team_name]


def rank_by_rating(stats, descending=True):
    """Sorts stat lines into a leaderboard by impact rating.

    Uses a custom sort key (the calculated rating) rather than sorting
    by any field that already exists on the record.

    Parameters:
        stats (list[PlayerMatchStat]): The stat lines to rank.
        descending (bool): Highest rating first when True (the default).

    Returns:
        list[PlayerMatchStat]: The same stat lines, sorted by rating.
    """
    return sorted(stats, key=rate_player_stat, reverse=descending)


def rank_by_goal_contributions(stats):
    """Sorts stat lines by goals first, using assists to break ties.

    Demonstrates a custom key built from more than one field: Python's
    sort is stable, but a tuple key lets us express "goals, then assists"
    directly instead of relying on sort stability.

    Parameters:
        stats (list[PlayerMatchStat]): The stat lines to rank.

    Returns:
        list[PlayerMatchStat]: The same stat lines, sorted by (goals, assists) descending.
    """
    return sorted(stats, key=lambda s: (s.goals, s.assists), reverse=True)


def build_report_lines(stats, title):
    """Builds the text lines of a report for a given set of stat lines.

    The stat lines are reported in the order given, so callers who want a
    leaderboard should sort (e.g. with rank_by_rating) before calling this.

    Parameters:
        stats (list[PlayerMatchStat]): The stat lines to report on.
        title (str): A heading for the report.

    Returns:
        list[str]: The report, one line per entry, ready to print or save.
    """
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
    """Writes a report for the given stat lines out to a text file.

    Parameters:
        stats (list[PlayerMatchStat]): The stat lines to report on.
        title (str): A heading for the report.
        filepath (str): Where to save the report.
    """
    lines = build_report_lines(stats, title)
    with open(filepath, "w") as out_file:
        out_file.write("\n".join(lines) + "\n")
