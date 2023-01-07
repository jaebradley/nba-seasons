from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Team:
    name: str
    first_season_start_year: int
    last_season_start_year: int

    def __post_init__(self):
        if 0 >= self.first_season_start_year:
            raise ValueError("First season start year must be positive")

        if 0 >= self.last_season_start_year:
            raise ValueError("Last season start year must be positive")

        if 0 >= len(self.name):
            raise ValueError("Name cannot be empty")


@dataclass(frozen=True)
class Franchise:
    name: str
    first_season_start_year: int
    last_season_start_year: int

    def __post_init__(self):
        if 0 >= self.first_season_start_year:
            raise ValueError("First season start year must be positive")

        if 0 >= self.last_season_start_year:
            raise ValueError("Last season start year must be positive")

        if 0 >= len(self.name):
            raise ValueError("Name cannot be empty")


@dataclass(frozen=True)
class Season:
    start_year: int
    champion: Optional[str]

    def __post_init__(self):
        if 0 >= self.start_year:
            raise ValueError("Start year must be positive")

        if self.champion is not None and 0 >= len(self.champion):
            raise ValueError("Champion name cannot be empty")
