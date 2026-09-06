"""Builds and prints post-match and season reports.

This module has one job: turn a list of PlayerMatchStat + rating pairs
into a readable report. It does not load data or calculate ratings itself.
"""

from ratings import rate_player_stat


def filter_by_match(stats, match_id):
    """Returns only the stat lines belonging to a given match.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        match_id (int): The match to filter for.

    Returns:
        list[PlayerMatchStat]: Stat lines for that match only.
    """
    return [s for s in stats if s.match_id == match_id]


def filter_by_team(stats, team_name):
    """Returns only the stat lines belonging to a given team, across all matches.

    Parameters:
        stats (list[PlayerMatchStat]): All loaded stat lines.
        team_name (str): The team to filter for.

    Returns:
        list[PlayerMatchStat]: Stat lines for that team only.
    """
    return [s for s in stats if s.team == team_name]


def build_report_lines(stats, title):
    """Builds the text lines of a report for a given set of stat lines.

    Parameters:
        stats (list[PlayerMatchStat]): The stat lines to report on.
        title (str): A heading for the report.

    Returns:
        list[str]: The report, one line per entry, ready to print or save.
    """
    lines = [f"=== {title} ==="]
    for stat in stats:
        rating = rate_player_stat(stat)
        lines.append(
            f"{stat.player_name:<20} {stat.position:<3} {stat.team:<15} "
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
