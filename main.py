"""Entry point: loads match data and generates post-match and season reports."""

from data_loader import load_match_stats
from report import filter_by_match, filter_by_team, print_report, save_report

DATA_PATH = "../data/soccer_match_stats.csv"


def main():
    """Loads the dataset and produces a sample match report and team report."""
    stats = load_match_stats(DATA_PATH)

    match_1_stats = filter_by_match(stats, match_id=1)
    print_report(match_1_stats, title="Match 1 Report")
    save_report(match_1_stats, title="Match 1 Report", filepath="match_1_report.txt")

    print()
    charlotte_stats = filter_by_team(stats, team_name="Charlotte FC")
    print_report(charlotte_stats, title="Charlotte FC Season Report")


if __name__ == "__main__":
    main()
