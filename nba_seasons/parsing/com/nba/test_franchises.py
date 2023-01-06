from unittest import TestCase

from nba_seasons.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser
from nba_seasons.parsing.com.nba.franchises import Parser, RecordHandler


class Test(TestCase):
    def test_parse(self):
        with open(
                "/Users/jaebradley/projects/nba-seasons/nba_seasons/data/com/basketball_reference/teams/2022-06-22.html",
                "r") as file:
            records = list()
            parser = FranchiseAndTeamParser(lambda record: records.append(record))
            parser.feed(data=file.read())
            parser.close()

            parser = Parser(record_handler=RecordHandler(lambda start_year: int(start_year.split("-")[0])))
            history = parser.parse(records=records)

            self.assertIsNotNone(history)
