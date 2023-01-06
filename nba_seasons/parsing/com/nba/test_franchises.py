from unittest import TestCase

from franchises import Parser, RecordHandler
from src.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser


class Test(TestCase):
    def test_parse(self):
        with open("/Users/jaebradley/projects/nba-seasons/src/data/com/basketball_reference/teams/2022-06-22.html",
                  "r") as file:
            records = list()
            parser = FranchiseAndTeamParser(lambda record: records.append(record))
            parser.feed(data=file.read())
            parser.close()

            parser = Parser(record_handler=RecordHandler(lambda start_year: int(start_year.split("-")[0])))
            history = parser.parse(records=records)

            self.assertIsNotNone(history)
