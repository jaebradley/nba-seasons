from typing import Dict, Set

from nba_seasons.models.basketball_reference import FranchiseName, TeamName
from nba_seasons.models.calendar import GregorianCalendarCommonEraYearCount
from nba_seasons.parsing.com.basketball_reference.models import Team, Franchise
from nba_seasons.parsing.com.basketball_reference.seasons import Season


def translate_franchise(history: Dict[Franchise, Set[Team]]) -> Dict[
    GregorianCalendarCommonEraYearCount,
    Dict[FranchiseName, TeamName]]:
    franchise_and_team_by_starting_season = dict({})

    for franchise, teams in history.items():
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

    return {
        GregorianCalendarCommonEraYearCount(value=key): {
            FranchiseName(value=franchise_name): TeamName(value=team_name)
            for franchise_name, team_name in value.items()
        } for key, value in franchise_and_team_by_starting_season.items()}


def filter_franchises(
        seasons: Set[Season],
        franchises_and_team_by_starting_season: Dict[
            GregorianCalendarCommonEraYearCount, Dict[FranchiseName, TeamName]]) -> Dict[
    GregorianCalendarCommonEraYearCount, Dict[FranchiseName, TeamName]]:
    season_start_years = set(map(lambda season: season.start_year, seasons))
    return {key: value for key, value in franchises_and_team_by_starting_season.items() if
            key.value in season_start_years}
