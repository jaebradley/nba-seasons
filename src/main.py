import os.path
from pathlib import Path

from src.parsing.com.basketball_reference.seasons import parse as parse_seasons
from src.parsing.com.nba.franchises import parse as parse_franchises
from src.writing.com.basketball_reference.seasons import LeagueTranslator, LeagueWriter


def main():
    with open("../src/data/com/basketball_reference/teams/2022-06-22.html", "r") as franchises_file:
        franchise_history = parse_franchises(franchises_file.read())

        with open("../src/data/com/basketball_reference/seasons/2022-05-20.html", "r") as seasons_file:
            seasons = parse_seasons(seasons_file.read())
            current_directory = str(Path(__file__).resolve().parent)

            league = LeagueTranslator().translate(seasons=seasons, history=franchise_history)
            os.makedirs(current_directory + "/data/output", exist_ok=True)
            LeagueWriter(output_directory_path=current_directory + "/data/output").write(league=league)


if __name__ == '__main__':
    main()
