"""Entry point: loads data, rates it, and runs the full suite of reports/charts."""

from data_loader import load_match_stats
from report import (
    filter_by_match,
    filter_by_team,
    rank_by_rating,
    team_average_rating_by_position,
    player_form,
    home_away_split,
    stat_correlations_with_rating,
    print_report,
    save_report,
    plot_top_performers,
    plot_player_form,
)

DATA_PATH = "../data/soccer_match_stats.csv"
STAT_NAMES = ["goals", "assists", "tackles_won", "saves", "passes_completed", "minutes_played"]


def main():
    """Loads the dataset and prints/saves the full analysis suite."""
    stats = load_match_stats(DATA_PATH)

    match_1_stats = filter_by_match(stats, match_id=1)
    leaderboard = rank_by_rating(match_1_stats)
    print_report(leaderboard, title="Match 1 Leaderboard")
    save_report(leaderboard, title="Match 1 Leaderboard", filepath="match_1_leaderboard.txt")

    print("\n=== Charlotte FC: Avg. Rating by Position ===")
    for position, avg in team_average_rating_by_position(stats, "Charlotte FC").items():
        print(f"{position}: {avg}")

    print("\n=== Charlotte FC: Home vs. Away Avg. Rating ===")
    for venue, avg in home_away_split(stats, "Charlotte FC").items():
        print(f"{venue}: {avg}")

    print("\n=== Wilfried Zaha: Form (3-match rolling average) ===")
    for match_date, opponent, rating, form_rating in player_form(stats, "Wilfried Zaha", window=3):
        print(f"{match_date}  vs {opponent:<15}  rating: {rating:<6}  form: {form_rating}")

    print("\n=== Which stats correlate most with impact rating? ===")
    for stat_name, corr in stat_correlations_with_rating(stats, STAT_NAMES):
        print(f"{stat_name}: {corr}")

    plot_top_performers(stats, team_name="Charlotte FC", top_n=8, output_path="charlotte_fc_top_performers.png")
    plot_player_form(stats, player_name="Wilfried Zaha", window=3, output_path="zaha_form.png")
    print("\nSaved charts -> charlotte_fc_top_performers.png, zaha_form.png")


if __name__ == "__main__":
    main()
