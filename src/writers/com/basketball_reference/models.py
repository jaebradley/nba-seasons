from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=False, unsafe_hash=True)
class Season:
    next_season: Optional['Season'] = field(hash=False)
    offset_in_years: int = field(hash=False)
    duration_in_years: Optional[int] = field(hash=False)
    starting_year: int = field(hash=True)
    team_name_by_franchise_names: Dict[str, str]

    def __post_init__(self):
        if 0 > self.offset_in_years:
            raise ValueError("Offset in years must be non-negative")

        if 0 >= self.starting_year:
            raise ValueError("Starting year must be positive")

        if len(set(self.team_name_by_franchise_names.values())) != len(self.team_name_by_franchise_names):
            raise ValueError("Duplicate team names exist")


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
