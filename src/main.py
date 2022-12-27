import os.path
from pathlib import Path

from src.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser
from src.parsing.com.basketball_reference.seasons import parse as parse_seasons
from src.parsing.com.nba.franchises import Parser, RecordHandler, deserialize_start_year, generate_teams_by_franchise, \
    handle_single_team_franchise
from src.translators.com.basketball_reference.franchise import translate_franchise, filter_franchises
from src.translators.com.basketball_reference.league import translate_league
from src.writers.com.basketball_reference.seasons import LeagueWriter


def main():
    with open("../src/data/com/basketball_reference/teams/2022-06-22.html", "r") as franchises_file:
        records = list()
        parser = FranchiseAndTeamParser(lambda record: records.append(record))
        parser.feed(data=franchises_file.read())
        parser.close()
        p = parser = Parser(
            teams_by_franchise_generator=generate_teams_by_franchise,
            single_team_franchise_handler=handle_single_team_franchise
        )
        history = parser.parse(records=RecordHandler(
            start_year_deserializer=deserialize_start_year,
            records=list(filter(lambda record: "NBA" in record.league_name, records))
        ))

    with open("../src/data/com/basketball_reference/seasons/2022-05-20.html", "r") as seasons_file:
        seasons = parse_seasons(seasons_file.read())
        current_directory = str(Path(__file__).resolve().parent)
        franchise_and_team_by_starting_season = filter_franchises(
            seasons=seasons,
            franchises_and_team_by_starting_season=translate_franchise(history=history))

        league = translate_league(franchise_and_team_by_starting_season=franchise_and_team_by_starting_season)
        os.makedirs(current_directory + "/data/output", exist_ok=True)
        LeagueWriter(output_directory_path=current_directory + "/data/output").write(league=league)


if __name__ == '__main__':
    main()
