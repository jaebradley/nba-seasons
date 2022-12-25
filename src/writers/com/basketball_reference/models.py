from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


class SeasonIterator:
    def __init__(self, starting_season: Season):
        self.current_season = starting_season

    def __iter__(self):
        return self.current_season

    def __next__(self):
        if self.current_season is None:
            raise StopIteration

        current_season = self.current_season
        self.current_season = self.current_season.next_season
        return current_season


@dataclass(frozen=False)
class Season:
    next_season: Optional['Season'] = field(hash=False)
    offset_in_years: int = field(hash=False)
    duration_in_years: Optional[int] = field(hash=False)
    team_name_by_franchise_names: Dict[str, str]

    def __post_init__(self):
        if 0 > self.offset_in_years:
            raise ValueError("Offset in years must be non-negative")

        if len(set(self.team_name_by_franchise_names.values())) != len(self.team_name_by_franchise_names):
            raise ValueError("Duplicate team names exist")

        if self.duration_in_years is None and self.next_season is not None:
            raise ValueError("If a next season exists then a duration must also exist")

    def __iter__(self):
        return SeasonIterator(starting_season=self)


@dataclass(frozen=True, eq=True)
class League:
    name: str
    start_year: int
    inaugural_season: Season

    def __post_init__(self):
        if 0 >= len(self.name):
            raise ValueError("Name cannot be empty")

        if 0 >= self.start_year:
            raise ValueError("Start year must be positive")
