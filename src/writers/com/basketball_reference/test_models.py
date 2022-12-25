from unittest import TestCase

from .models import Season


class TestSeason(TestCase):
    def test_duplicate_team_names_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Season(
                next_season=None,
                offset_in_years=0,
                duration_in_years=0,
                team_name_by_franchise_names={
                    "foo": "bar",
                    "baz": "bar"
                }
            )

            self.assertEqual("Duplicate team names exist", str(context.exception))

    def test_single_iteration_for_single_season(self):
        seasons = Season(
            next_season=None,
            offset_in_years=0,
            duration_in_years=0,
            team_name_by_franchise_names={
                "foo": "foo",
                "baz": "baz"
            }
        )
        counter = 0
        for _ in seasons:
            counter += 1

        self.assertEqual(1, counter)

    def test_two_iterations_for_two_seasons(self):
        seasons = Season(
            next_season=Season(
                next_season=None,
                offset_in_years=1,
                duration_in_years=2,
                team_name_by_franchise_names=dict({})
            ),
            offset_in_years=0,
            duration_in_years=0,
            team_name_by_franchise_names={
                "foo": "foo",
                "baz": "baz"
            }
        )
        counter = 0
        for _ in seasons:
            counter += 1

        self.assertEqual(2, counter)
