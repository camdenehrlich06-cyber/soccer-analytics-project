"""Entry point: loads data into a DataFrame, rates it, reports it, and charts it."""

from data_loader import load_match_stats
from ratings import add_impact_rating_column
from report import match_leaderboard, team_average_rating_by_position, plot_top_performers

DATA_PATH = "../data/soccer_match_stats.csv"


def main():
    """Loads the dataset, adds ratings, prints two reports, and saves a chart."""
    df = load_match_stats(DATA_PATH)
    df = add_impact_rating_column(df)

    print("=== Match 1 Leaderboard ===")
    leaderboard = match_leaderboard(df, match_id=1)
    print(leaderboard[["player_name", "team", "position", "impact_rating"]].to_string(index=False))

    print("\n=== Charlotte FC: Avg. Rating by Position ===")
    print(team_average_rating_by_position(df, "Charlotte FC").round(2).to_string())

    plot_top_performers(df, team_name="Charlotte FC", top_n=8, output_path="charlotte_fc_top_performers.png")
    print("\nSaved chart -> charlotte_fc_top_performers.png")


if __name__ == "__main__":
    main()
