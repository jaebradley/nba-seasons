from unittest import TestCase

from nba_seasons.models.basketball_reference import Season, FranchiseName, TeamName
from nba_seasons.models.iso_8601 import YearDuration


class TestSeason(TestCase):
    def test_duplicate_team_names_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Season(
                previous_season=None,
                offset=YearDuration(value=0),
                duration=YearDuration(value=0),
                team_name_by_franchise_names={
                    FranchiseName(value="foo"): TeamName(value="bar"),
                    FranchiseName(value="baz"): TeamName(value="bar"),
                }
            )

            self.assertEqual("Duplicate team names exist", str(context.exception))

    def test_single_iteration_for_single_season(self):
        seasons = Season(
            previous_season=None,
            offset=YearDuration(value=0),
            duration=YearDuration(value=0),
            team_name_by_franchise_names={
                FranchiseName(value="foo"): TeamName(value="foo"),
                FranchiseName(value="baz"): TeamName(value="baz"),
            }
        )
        counter = 0
        for _ in seasons:
            counter += 1

        self.assertEqual(1, counter)

    def test_two_iterations_for_two_seasons(self):
        seasons = Season(
            previous_season=Season(
                previous_season=None,
                offset=YearDuration(value=1),
                duration=YearDuration(value=2),
                team_name_by_franchise_names=dict({})
            ),
            offset=YearDuration(value=0),
            duration=YearDuration(value=0),
            team_name_by_franchise_names={
                FranchiseName(value="foo"): TeamName(value="foo"),
                FranchiseName(value="baz"): TeamName(value="baz"),
            }
        )
        counter = 0
        for _ in seasons:
            counter += 1

        self.assertEqual(2, counter)
