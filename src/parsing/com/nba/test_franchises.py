from unittest import TestCase

from franchises import Parser, RecordHandler, deserialize_start_year, generate_teams_by_franchise, \
    handle_single_team_franchise
from src.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser


class Test(TestCase):
    def test_parse(self):
        with open("/Users/jaebradley/projects/nba-seasons/src/data/com/basketball_reference/teams/2022-06-22.html",
                  "r") as file:
            records = list()
            parser = FranchiseAndTeamParser(lambda record: records.append(record))
            parser.feed(data=file.read())
            parser.close()

            parser = Parser(
                teams_by_franchise_generator=generate_teams_by_franchise,
                single_team_franchise_handler=handle_single_team_franchise
            )
            history = parser.parse(records=RecordHandler(
                start_year_deserializer=deserialize_start_year,
                records=list(filter(lambda record: "NBA" in record.league_name, records))
            ))

            self.assertIsNotNone(history)
