from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Set, Dict, Optional

from src.parsing.com.basketball_reference.seasons import Season as ParsedSeason
from src.parsing.com.nba.franchises import FranchiseHistory


@dataclass(frozen=False, unsafe_hash=True)
class Season:
    next_season: Optional['Season'] = field(hash=False)
    offset_in_years: int = field(hash=False)
    duration_in_years: int = field(hash=False)
    starting_year: int = field(hash=True)
    team_name_by_franchise_names: Dict[str, str]


@dataclass(frozen=True, eq=True)
class League:
    name: str
    start_year: int
    inaugural_season: Season


class LeagueTranslator:
    def translate(self, seasons: Set[ParsedSeason], history: FranchiseHistory) -> League:
        sorted_seasons = sorted(seasons, key=lambda season: season.start_year)
        previous_season_end_year = sorted_seasons[0].start_year
        previous_season = None
        first_season = None

        for season in sorted_seasons:
            team_name_by_franchise_names = dict({})

            for franchise, teams in history.history.items():
                for team in teams:
                    if team.first_season_start_year <= season.start_year <= team.last_season_start_year:
                        if franchise.name in team_name_by_franchise_names:
                            if franchise.name == "New Orleans Pelicans":
                                team_name_by_franchise_names[franchise.name] = "NO/Ok. City Hornets"
                            else:
                                raise ValueError("Franchise team already found")
                        else:
                            team_name_by_franchise_names[franchise.name] = team.name

            current_season = Season(
                offset_in_years=season.start_year - previous_season_end_year,
                duration_in_years=1,
                next_season=None,
                starting_year=season.start_year,
                team_name_by_franchise_names=team_name_by_franchise_names
            )
            if first_season is None:
                first_season = current_season
            if previous_season is not None:
                previous_season.next_season = current_season
            previous_season_end_year = season.start_year + current_season.duration_in_years
            previous_season = current_season

        return League(
            name="National Basketball Association",
            start_year=sorted_seasons[0].start_year,
            inaugural_season=first_season
        )


class LeagueWriter:

    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path

    def write(self, league: League):
        with open(self.output_directory_path + "/" + league.name + ".yaml", 'w', encoding="utf-8") as output_file:
            output_file.write("starting year: " + str(league.start_year) + "\n")
            output_file.write("seasons: \n")
            current_season = league.inaugural_season
            while current_season is not None:
                output_file.write("  - offset in years: " + str(current_season.offset_in_years) + "\n")
                output_file.write("    duration in years: " + str(current_season.duration_in_years) + "\n")
                output_file.write("    team name by franchise names: \n")

                for franchise_name, team_name in OrderedDict(sorted(current_season.team_name_by_franchise_names.items())).items():
                    output_file.write("      " + franchise_name + ": " + team_name + "\n")

                current_season = current_season.next_season
