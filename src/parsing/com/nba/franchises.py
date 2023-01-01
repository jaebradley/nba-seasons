from itertools import groupby
from typing import Set, Dict, Tuple, List, Callable, Optional

from src.parsing.com.basketball_reference.franchises import Record
from src.parsing.com.basketball_reference.models import Team, Franchise


def deserialize_start_year(value: str) -> Optional[int]:
    parts = value.split("-")
    if 2 != len(parts):
        return None
    try:
        return int(parts[0])
    except ValueError:
        return None


class RecordHandler:
    def __init__(self, start_year_deserializer: Callable[[str], Optional[int]], records: List[Record]):
        self.start_year_deserializer = start_year_deserializer
        self.records = records
        self.current_franchise = None
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[Franchise, Optional[Team]]:
        if self.current_index >= len(self.records):
            raise StopIteration

        value = self.handle(record=self.records[self.current_index])
        self.current_index += 1

        return value

    def handle(self, record: Record) -> Tuple[Franchise, Optional[Team]]:
        first_season_start_year = self.start_year_deserializer(record.first_season_start_year)
        if first_season_start_year is None:
            raise ValueError(f"Could not deserialize start year value: {record.first_season_start_year}")
        last_season_start_year = self.start_year_deserializer(record.last_season_start_year)
        if last_season_start_year is None:
            raise ValueError(f"Could not deserialize start year value: {record.last_season_start_year}")

        team = None
        if record.type is Record.Type.FRANCHISE:
            self.current_franchise = Franchise(
                name=record.name,
                first_season_start_year=first_season_start_year,
                last_season_start_year=last_season_start_year
            )
        elif record.type is Record.Type.TEAM:
            team = Team(
                name=record.name,
                first_season_start_year=first_season_start_year,
                last_season_start_year=last_season_start_year
            )
        else:
            raise ValueError(f"Unexpected record type: {record.Type.name}")

        return self.current_franchise, team


def generate_teams_by_franchise(record_handler: RecordHandler) -> Dict[Franchise, Set[Team]]:
    return dict([
        (franchise, set([team for franchise, team in teams if team is not None]))
        for (franchise, teams) in groupby(
            list(record_handler),
            lambda team_by_franchise: team_by_franchise[0])
    ])


def handle_single_team_franchise(franchise: Franchise) -> Set[Team]:
    return {Team(name=franchise.name,
                 first_season_start_year=franchise.first_season_start_year,
                 last_season_start_year=franchise.last_season_start_year)}


class Parser:
    def __init__(self,
                 teams_by_franchise_generator: Callable[[RecordHandler], Dict[Franchise, Set[Team]]],
                 single_team_franchise_handler: Callable[[Franchise], Set[Team]]):
        self.teams_by_franchise_generator = teams_by_franchise_generator
        self.single_team_franchise_handler = single_team_franchise_handler

    def parse(self, records: RecordHandler) -> Dict[Franchise, Set[Team]]:
        return dict(
            map(
                lambda entry: (
                    entry[0],
                    self.single_team_franchise_handler(entry[0])
                    if len(entry[1]) <= 0 else entry[1]),
                self.teams_by_franchise_generator(records).items()
            )
        )
