from itertools import groupby
from typing import Set, Dict, Tuple, List, Callable, Optional

from nba_seasons.parsing.com.basketball_reference.franchises import Record
from nba_seasons.parsing.com.basketball_reference.models import Team, Franchise


class RecordHandler:
    def __init__(self, start_year_deserializer: Callable[[str], int]):
        self.start_year_deserializer = start_year_deserializer
        self.current_franchise = None

    def handle(self, record: Record) -> Tuple[Franchise, Optional[Team]]:
        first_season_start_year = self.start_year_deserializer(record.first_season_start_year)
        last_season_start_year = self.start_year_deserializer(record.last_season_start_year)

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
            raise ValueError

        return self.current_franchise, team


class Parser:
    def __init__(self, record_handler):
        self.record_handler = record_handler

    def parse(self, records: List[Record]) -> Dict[Franchise, Set[Team]]:
        return dict(
            map(
                lambda entry: (entry[0], set([Team(name=entry[0].name,
                                                   first_season_start_year=entry[0].first_season_start_year,
                                                   last_season_start_year=entry[0].last_season_start_year)]) if len(
                    entry[1]) <= 0 else entry[1]),
                dict([(label, set([v for l, v in value if v is not None])) for (label, value) in groupby(
                    map(
                        lambda record: self.record_handler.handle(record=record),
                        filter(lambda record: "NBA" in record.league_name, records)
                    ), lambda x: x[0])]).items()
            )
        )
