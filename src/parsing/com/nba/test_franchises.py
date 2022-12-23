from unittest import TestCase
from franchises import parse


class Test(TestCase):
    def test_parse(self):
        with open("/Users/jaebradley/projects/nba-seasons/src/data/com/basketball_reference/teams/2022-06-22.html", "r") as file:
            history = parse(file.read())

            self.assertIsNotNone(history)