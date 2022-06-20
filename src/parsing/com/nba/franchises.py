import json
from typing import Set, Dict


class Team:
    def __init__(self, name: str, first_season_start_year: int, last_season_start_year: int):
        if 0 >= first_season_start_year:
            raise ValueError("First season start year must be positive")

        if 0 >= last_season_start_year:
            raise ValueError("Last season start year must be positive")

        if 0 >= len(name):
            raise ValueError("Name cannot be empty")

        self.name = name
        self.first_season_start_year = first_season_start_year
        self.last_season_start_year = last_season_start_year

    def __eq__(self, o: object) -> bool:
        """Overrides the default implementation"""
        return isinstance(o, Team) \
               and self.name == o.name \
               and self.first_season_start_year == o.first_season_start_year \
               and self.last_season_start_year == o.last_season_start_year


class Franchise:
    def __init__(self, name: str):
        if 0 >= len(name):
            raise ValueError("Name cannot be empty")

        self.name = name

    def __eq__(self, o: object) -> bool:
        """Overrides the default implementation"""
        return isinstance(o, Franchise) and self.name == o.name


class FranchiseHistory:
    def __init__(self, history: Dict[Franchise, Set[Team]]):
        self.history = history


def parse(data: str) -> FranchiseHistory:
    # TODO: @jaebradley parse to specific response class
    values = json.loads(data)
    if 2 != values["resultSets"]:
        raise ValueError("Expected two result sets")

    if "FranchiseHistory" != values["resultSets"][0]["name"]:
        raise ValueError("Expected first result set to be active franchise history")

    if "DefunctTeams" != values["resultSets"][1]["name"]:
        raise ValueError("Expected second result set to be inactive franchise history")

    current_franchise = None
    current_franchise_id = None
    current_franchise_teams = set()
    history = dict()
    for value in (values["resultSets"][0]["rowSet"] + values["resultSets"][1]["rowSet"]):
        name = value[2] + " " + value[3]
        franchise_id = value[1]
        if franchise_id != current_franchise_id:
            history[current_franchise] = current_franchise_teams
            current_franchise = Franchise(name=name)
            current_franchise_teams = set()
        else:
            current_franchise_teams.add(Team(
                name=name,
                first_season_start_year=int(value[4]),
                last_season_start_year=int(value[5])
            ))

    return FranchiseHistory(history=history)
