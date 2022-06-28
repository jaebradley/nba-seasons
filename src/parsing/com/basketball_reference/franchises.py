from __future__ import annotations

import enum
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Callable


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


@dataclass(unsafe_hash=True)
class Record:
    class Type(enum.Enum):
        FRANCHISE = "FRANCHISE",
        TEAM = "TEAM"

    name: str
    type: Type
    league_name: str = ""
    first_season_start_year: str = ""
    last_season_start_year: str = ""


class FranchiseAndTeamParser(HTMLParser):
    EXPECTED_FRANCHISE_NAME_ATTRIBUTES = {('scope', 'row'), ('class', 'left '), ('data-stat', 'franch_name')}
    EXPECTED_TEAM_NAME_ATTRIBUTES = {('scope', 'row'), ('class', 'right '), ('data-stat', 'team_name')}
    EXPECTED_LEAGUE_ID_ATTRIBUTES = {('class', 'left '), ('data-stat', 'lg_id')}
    EXPECTED_FIRST_SEASON_START_YEAR_ATTRIBUTES = {('class', 'right '), ('data-stat', 'year_min')}
    EXPECTED_LAST_SEASON_START_YEAR_ATTRIBUTES = {('class', 'right '), ('data-stat', 'year_max')}

    class AttributeType(enum.Enum):
        NAME = "NAME",
        LEAGUE_NAME = "LEAGUE_NAME"
        FIRST_SEASON_START_YEAR = "FIRST_SEASON_START_YEAR"
        LAST_SEASON_START_YEAR = "LAST_SEASON_START_YEAR"

    def __init__(self, consumer: Callable[[Record], None]):
        super().__init__()
        self.consumer = consumer
        self.record_type = None
        self.attribute_type = None
        self.record = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if "th" == tag:
            if set(attrs) == self.EXPECTED_FRANCHISE_NAME_ATTRIBUTES:
                self.record_type = Record.Type.FRANCHISE
                self.attribute_type = self.AttributeType.NAME
            elif set(attrs) == self.EXPECTED_TEAM_NAME_ATTRIBUTES:
                self.record_type = Record.Type.TEAM
                self.attribute_type = self.AttributeType.NAME
        elif "td" == tag:
            if set(attrs) == self.EXPECTED_LEAGUE_ID_ATTRIBUTES:
                self.attribute_type = self.AttributeType.LEAGUE_NAME
            elif set(attrs) == self.EXPECTED_FIRST_SEASON_START_YEAR_ATTRIBUTES:
                self.attribute_type = self.AttributeType.FIRST_SEASON_START_YEAR
            elif set(attrs) == self.EXPECTED_LAST_SEASON_START_YEAR_ATTRIBUTES:
                self.attribute_type = self.AttributeType.LAST_SEASON_START_YEAR

    def handle_data(self, data: str) -> None:
        if self.record_type is not None and self.attribute_type is not None:
            if self.record is None:
                self.record = Record(name=data, type=self.record_type)
            else:
                if self.AttributeType.LEAGUE_NAME is self.attribute_type:
                    self.record.league_name = data
                elif self.AttributeType.FIRST_SEASON_START_YEAR is self.attribute_type:
                    self.record.first_season_start_year = data
                elif self.AttributeType.LAST_SEASON_START_YEAR is self.attribute_type:
                    self.record.last_season_start_year = data
                    self.consumer(self.record)
                    self.record = None
                    self.attribute_type = None
