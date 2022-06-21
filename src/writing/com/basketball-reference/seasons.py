from typing import Set

from src.parsing.com.basketball_reference.seasons import Season
from src.parsing.com.nba.franchises import FranchiseHistory


def write_seasons(directory_path: str, seasons: Set[Season], history: FranchiseHistory):
    for season in seasons:
        with open(
                directory_path + "/" + str(season.start_year),
                'x',
                encoding="utf-8"
        ) as file:
            season_teams = set()

            for franchise, teams in history.history.items():
                franchise_season_teams = set(
                    filter(
                        lambda team: team.first_season_start_year >= season.start_year > team.last_season_start_year,
                        teams
                    )
                )

                if 1 < len(franchise_season_teams):
                    raise ValueError("Expected at most 1 team per franchise per season")

                season_teams.update(franchise_season_teams)

            team_names = set(map(lambda team: team.name, season_teams))
            if season.champion not in team_names:
                raise ValueError(season.champion + " is not in teams for season")

            file.write(
                ",".join(sorted(team_names))
            )

            file.write(season.champion)
