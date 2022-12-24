from unittest import TestCase

from .models import Season


class TestSeason(TestCase):
    def test_duplicate_team_names_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Season(
                next_season=None,
                offset_in_years=0,
                duration_in_years=0,
                starting_year=1,
                team_name_by_franchise_names={
                    "foo": "bar",
                    "baz": "bar"
                }
            )

            self.assertEqual("Duplicate team names exist", str(context.exception))
