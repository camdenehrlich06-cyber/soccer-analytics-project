import csv

def load_data(filename):
    data = []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def calculate_impact_rating(goals, assists, tackles_won, minutes_played, saves):
    raw_score = (goals * 4) + (assists * 3) + (tackles_won * 1) + (saves * 1.5)
    if minutes_played == 0:
        return 0.0
    per_90 = raw_score * (90 / minutes_played)
    if per_90 > 10:
        per_90 = 10
    return round(per_90, 2)

def print_match_report(data, match_id):
    print(f"\n=== Match {match_id} Report ===")
    for row in data:
        if int(row["match_id"]) == match_id:
            rating = calculate_impact_rating(
                int(row["goals"]),
                int(row["assists"]),
                int(row["tackles_won"]),
                int(row["minutes_played"]),
                int(row["saves"]),
            )
            print(row["player_name"], row["team"], "-> rating:", rating)

def print_team_report(data, team_name):
    print(f"\n=== {team_name} Season Report ===")
    for row in data:
        if row["team"] == team_name:
            rating = calculate_impact_rating(
                int(row["goals"]),
                int(row["assists"]),
                int(row["tackles_won"]),
                int(row["minutes_played"]),
                int(row["saves"]),
            )
            print(row["player_name"], "match", row["match_id"], "-> rating:", rating)

def main():
    data = load_data("../data/soccer_match_stats.csv")
    print_match_report(data, 1)
    print_team_report(data, "Charlotte FC")

if __name__ == "__main__":
    main()
