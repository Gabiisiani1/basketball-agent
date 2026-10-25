"""ხელსაწყოები (tools) ბასკეტბოლის აგენტისთვის."""
import csv
from pathlib import Path

from smolagents import tool

DATA_FILE = Path(__file__).parent / "data" / "games.csv"

# სვეტები, რომელზეც საშუალოს დათვლა აზრიანია
STATS = [
    "minutes", "points", "rebounds", "assists", "steals", "blocks",
    "turnovers", "fouls", "fgm", "fga", "tpm", "tpa", "ftm", "fta",
]


def _load_games() -> list[dict]:
    """კითხულობს games.csv-ს და აბრუნებს თამაშების სიას თარიღის მიხედვით დალაგებულს."""
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: r["date"])
    return rows


@tool
def get_stat_average(stat: str, last_n_games: int) -> str:
    """Returns the average, total and number of games for one stat from the player's game log (box scores).

    Args:
        stat: The stat to compute. One of: minutes, points, rebounds, assists, steals, blocks, turnovers, fouls, fgm, fga, tpm, tpa, ftm, fta.
        last_n_games: How many of the most recent games to include. Use 0 to include all games.
    """
    stat = stat.strip().lower()
    if stat not in STATS:
        return f"ERROR: unknown stat '{stat}'. Valid stats: {', '.join(STATS)}."
    try:
        n = int(last_n_games)
    except (TypeError, ValueError):
        return "ERROR: last_n_games must be an integer (0 = all games)."
    if n < 0:
        return "ERROR: last_n_games cannot be negative."

    try:
        games = _load_games()
    except FileNotFoundError:
        return f"ERROR: game log file not found at {DATA_FILE}."
    if not games:
        return "ERROR: the game log is empty."

    if n > 0:
        games = games[-n:]

    values = [float(g[stat]) for g in games]
    total = sum(values)
    avg = total / len(values)
    return (
        f"stat={stat}; games={len(values)} "
        f"(from {games[0]['date']} to {games[-1]['date']}); "
        f"total={total:g}; average={avg:.2f}"
    )
