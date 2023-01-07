from unittest import TestCase
import os

from nba_seasons.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser
from nba_seasons.translators.com.basketball_reference.records import TranslateRecords, RecordHandler

FRANCHISES_FILE = os.path.join(os.path.dirname(__file__),
                               "../../../data/com/basketball_reference/teams/2022-06-22.html")


class Test(TestCase):
    def test_parse(self):
        with open(FRANCHISES_FILE, "r") as file:
            records = list()
            parser = FranchiseAndTeamParser(lambda record: records.append(record))
            parser.feed(data=file.read())
            parser.close()

            parser = TranslateRecords(record_handler=RecordHandler(lambda start_year: int(start_year.split("-")[0])))
            history = parser.translate(records=records)

            self.assertIsNotNone(history)
