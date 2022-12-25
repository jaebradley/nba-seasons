from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class NaturalNumber:
    value: int

    def __post_init__(self):
        if 0 > self.value:
            raise ValueError("Must have non-negative value")


@dataclass(frozen=True)
class PositiveInteger(NaturalNumber):
    def __post_init__(self):
        if 0 >= self.value:
            raise ValueError("Must have non-positive value")


@dataclass(frozen=True)
class GregorianCalendarCommonEraYearCount(PositiveInteger):
    pass


@dataclass(frozen=True)
class GregorianCalendarYearDuration(NaturalNumber):
    pass


class SeasonIterator:
    def __init__(self, starting_season: Season):
        self.current_season = starting_season

    def __iter__(self):
        return self.current_season

    def __next__(self):
        if self.current_season is None:
            raise StopIteration

        current_season = self.current_season
        self.current_season = self.current_season.previous_season
        return current_season


@dataclass(frozen=True)
class NonEmptyString:
    value: str

    def __post_init__(self):
        if 0 >= len(self.value):
            raise ValueError("String cannot be empty")


@dataclass(frozen=True)
class TeamName(NonEmptyString):
    pass


@dataclass(frozen=True)
class FranchiseName(NonEmptyString):
    pass


@dataclass(frozen=True)
class Season:
    previous_season: Optional['Season']
    offset: GregorianCalendarYearDuration
    duration: Optional[GregorianCalendarYearDuration]
    team_name_by_franchise_names: Dict[FranchiseName, TeamName]

    def __post_init__(self):
        if len(set(self.team_name_by_franchise_names.values())) != len(self.team_name_by_franchise_names):
            raise ValueError("Duplicate team names exist")

    def __iter__(self):
        return SeasonIterator(starting_season=self)


@dataclass(frozen=True, eq=True)
class League:
    name: NonEmptyString
    most_recent_season: Tuple[GregorianCalendarCommonEraYearCount, Season]
