import os.path
from pathlib import Path

from nba_seasons.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser
from nba_seasons.parsing.com.basketball_reference.seasons import parse as parse_seasons
from nba_seasons.translators.com.basketball_reference.franchise import translate_franchise, filter_franchises
from nba_seasons.translators.com.basketball_reference.league import translate_league
from nba_seasons.translators.com.basketball_reference.records import TranslateRecords, RecordHandler
from nba_seasons.writers.com.basketball_reference.seasons import LeagueWriter


def main():
    with open("../nba_seasons/data/com/basketball_reference/teams/2022-06-22.html", "r") as franchises_file:
        records = list()
        parser = FranchiseAndTeamParser(lambda record: records.append(record))
        parser.feed(data=franchises_file.read())
        parser.close()
        p = TranslateRecords(
            record_handler=RecordHandler(start_year_deserializer=lambda start_year: int(start_year.split("-")[0])))
        franchise_history = p.translate(records=records)

        with open("../nba_seasons/data/com/basketball_reference/seasons/2022-05-20.html", "r") as seasons_file:
            seasons = parse_seasons(seasons_file.read())
            current_directory = str(Path(__file__).resolve().parent)
            franchise_and_team_by_starting_season = filter_franchises(
                seasons=seasons,
                franchises_and_team_by_starting_season=translate_franchise(history=franchise_history))

            league = translate_league(franchise_and_team_by_starting_season=franchise_and_team_by_starting_season)
            os.makedirs(current_directory + "/data/output", exist_ok=True)
            LeagueWriter(output_directory_path=current_directory + "/data/output").write(league=league)


if __name__ == '__main__':
    main()
