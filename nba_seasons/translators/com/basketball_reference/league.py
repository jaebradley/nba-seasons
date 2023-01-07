from collections import OrderedDict
from typing import Dict

from nba_seasons.models.basketball_reference import FranchiseName, TeamName, League, Season
from nba_seasons.models.iso_8601 import Year
from nba_seasons.models.iso_8601 import YearDuration
from nba_seasons.models.strings import NonEmptyString


def translate_league(franchise_and_team_by_starting_season: Dict[
    Year,
    Dict[FranchiseName, TeamName]]) -> League:
    franchise_and_team_by_season = OrderedDict(
        dict(sorted(franchise_and_team_by_starting_season.items(), key=lambda entry: entry[0].value)))
    start_year = next(iter(franchise_and_team_by_season))
    previous_season_end_year = start_year
    first_season = None
    previous_season = None

    for season_start_year, team_name_by_franchise_names in franchise_and_team_by_season.items():
        current_season = Season(
            previous_season=previous_season,
            offset=YearDuration(value=season_start_year.value - previous_season_end_year.value),
            duration=YearDuration(value=1),
            team_name_by_franchise_names=team_name_by_franchise_names
        )
        if first_season is None:
            first_season = current_season

        previous_season = current_season
        previous_season_end_year = Year(
            value=season_start_year.value + current_season.duration.value)

    return League(
        name=NonEmptyString(value="National Basketball Association"),
        most_recent_season=(
            next(iter(dict(sorted(franchise_and_team_by_starting_season.items(), key=lambda entry: -entry[0].value)))),
            previous_season)
    )
