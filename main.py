"""Entry point: loads data, rates it, and runs the full suite of reports/charts."""

from data_loader import load_match_stats
from ratings import add_impact_rating_column
from report import (
    match_leaderboard,
    team_average_rating_by_position,
    player_form,
    home_away_split,
    stat_correlations_with_rating,
    plot_top_performers,
    plot_player_form,
)

DATA_PATH = "../data/soccer_match_stats.csv"
STAT_COLUMNS = ["goals", "assists", "tackles_won", "saves", "passes_completed", "minutes_played"]


def main():
    """Loads the dataset, adds ratings, and prints/saves the full analysis suite."""
    df = load_match_stats(DATA_PATH)
    df = add_impact_rating_column(df)

    print("=== Match 1 Leaderboard ===")
    leaderboard = match_leaderboard(df, match_id=1)
    print(leaderboard[["player_name", "team", "position", "impact_rating"]].to_string(index=False))

    print("\n=== Charlotte FC: Avg. Rating by Position ===")
    print(team_average_rating_by_position(df, "Charlotte FC").to_string())

    print("\n=== Charlotte FC: Home vs. Away Avg. Rating ===")
    print(home_away_split(df, "Charlotte FC").to_string())

    print("\n=== Wilfried Zaha: Form (3-match rolling average) ===")
    print(player_form(df, "Wilfried Zaha", window=3).to_string(index=False))

    print("\n=== Which stats correlate most with impact rating? ===")
    print(stat_correlations_with_rating(df, STAT_COLUMNS).round(3).to_string())

    plot_top_performers(df, team_name="Charlotte FC", top_n=8, output_path="charlotte_fc_top_performers.png")
    plot_player_form(df, player_name="Wilfried Zaha", window=3, output_path="zaha_form.png")
    print("\nSaved charts -> charlotte_fc_top_performers.png, zaha_form.png")


if __name__ == "__main__":
    main()
