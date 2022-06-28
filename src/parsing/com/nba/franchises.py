from dataclasses import dataclass
from typing import Set, Dict

from src.parsing.com.basketball_reference.franchises import FranchiseAndTeamParser, Record


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


class FranchiseHistory:
    def __init__(self, history: Dict[Franchise, Set[Team]]):
        self.history = history


def parse(data: str) -> FranchiseHistory:
    records = list()
    parser = FranchiseAndTeamParser(lambda record: records.append(record))
    parser.feed(data=data)
    parser.close()

    current_franchise = None
    history = dict()
    for record in records:
        if "NBA" in record.league_name:
            first_season_start_year = int(record.first_season_start_year.split("-")[0])
            last_season_start_year = int(record.last_season_start_year.split("-")[0])
            if current_franchise is None:
                if record.type is not Record.Type.FRANCHISE:
                    raise ValueError("Expected first record type to be a franchise record")

                current_franchise = Franchise(
                    name=record.name,
                    first_season_start_year=first_season_start_year,
                    last_season_start_year=last_season_start_year
                )
                history[current_franchise] = set()
            else:
                if record.type is Record.Type.FRANCHISE:
                    if 0 == len(history[current_franchise]):
                        history[current_franchise].add(
                            Team(
                                name=current_franchise.name,
                                first_season_start_year=current_franchise.first_season_start_year,
                                last_season_start_year=current_franchise.last_season_start_year
                            )
                        )
                    current_franchise = Franchise(
                        name=record.name,
                        first_season_start_year=first_season_start_year,
                        last_season_start_year=last_season_start_year
                    )
                    history[current_franchise] = set()
                elif record.type is Record.Type.TEAM:
                    history[current_franchise].add(
                        Team(
                            name=record.name,
                            first_season_start_year=first_season_start_year,
                            last_season_start_year=last_season_start_year
                        )
                    )
                else:
                    raise ValueError("Unknown record type")

    return FranchiseHistory(history=history)
