from collections import OrderedDict
from typing import Dict

from src.writers.com.basketball_reference.models import League, Season


def translate_league(franchise_and_team_by_starting_season: Dict[int, Dict[str, str]]) -> League:
    franchise_and_team_by_season = OrderedDict(
        dict(sorted(franchise_and_team_by_starting_season.items(), key=lambda entry: entry[0])))
    start_year = next(iter(franchise_and_team_by_season))
    previous_season_end_year = start_year
    first_season = None
    previous_season = None

    for season_start_year, team_name_by_franchise_names in franchise_and_team_by_season.items():
        current_season = Season(
            offset_in_years=season_start_year - previous_season_end_year,
            duration_in_years=1,
            next_season=None,
            team_name_by_franchise_names=team_name_by_franchise_names
        )
        if first_season is None:
            first_season = current_season

        if previous_season is not None:
            previous_season.next_season = current_season
        previous_season = current_season
        previous_season_end_year = season_start_year + current_season.duration_in_years

    return League(
        name="National Basketball Association",
        start_year=start_year,
        inaugural_season=first_season
    )
