from typing import Dict, Set

from src.parsing.com.basketball_reference.seasons import Season
from src.parsing.com.nba.franchises import FranchiseHistory


def translate_franchise(history: FranchiseHistory) -> Dict[int, Dict[str, str]]:
    franchise_and_team_by_starting_season = dict({})

    for franchise, teams in history.history.items():
        for team in teams:
            for season_start_year in range(team.first_season_start_year, team.last_season_start_year + 1):
                franchise_and_team = franchise_and_team_by_starting_season.get(season_start_year, dict({}))
                if franchise.name in franchise_and_team:
                    if franchise.name == "New Orleans Pelicans":
                        franchise_and_team[franchise.name] = "NO/Ok. City Hornets"
                    else:
                        raise ValueError("Franchise team already found")
                else:
                    franchise_and_team[franchise.name] = team.name
                franchise_and_team_by_starting_season[season_start_year] = franchise_and_team

    return franchise_and_team_by_starting_season


def filter_franchises(
        seasons: Set[Season],
        franchises_and_team_by_starting_season: Dict[int, Dict[str, str]]) -> Dict[int, Dict[str, str]]:
    season_start_years = set(map(lambda season: season.start_year, seasons))
    return {key: value for key, value in franchises_and_team_by_starting_season.items() if key in season_start_years}
