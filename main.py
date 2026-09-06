"""Entry point: loads match data and generates ranked leaderboard reports."""

from data_loader import load_match_stats
from report import filter_by_match, filter_by_team, rank_by_rating, print_report, save_report

DATA_PATH = "../data/soccer_match_stats.csv"


def main():
    """Loads the dataset and produces a match leaderboard and a team leaderboard."""
    stats = load_match_stats(DATA_PATH)

    match_1_stats = filter_by_match(stats, match_id=1)
    match_1_leaderboard = rank_by_rating(match_1_stats)
    print_report(match_1_leaderboard, title="Match 1 Leaderboard")
    save_report(match_1_leaderboard, title="Match 1 Leaderboard", filepath="match_1_leaderboard.txt")

    print()
    charlotte_stats = filter_by_team(stats, team_name="Charlotte FC")
    charlotte_leaderboard = rank_by_rating(charlotte_stats)
    print_report(charlotte_leaderboard, title="Charlotte FC Leaderboard (all matches)")


if __name__ == "__main__":
    main()
