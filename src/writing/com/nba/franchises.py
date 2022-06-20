import base64

from src.parsing.com.nba.franchises import FranchiseHistory


def write_franchises(directory_path: str, history: FranchiseHistory) -> None:
    for franchise in history.history.keys():
        with open(
                directory_path + "/" + str(base64.b64encode(franchise.name.encode(encoding="utf-8")), "utf-8"),
                'x',
                encoding="utf-8"
        ) as file:
            file.write("")


def write_teams(directory_path: str, history: FranchiseHistory) -> None:
    for franchise, teams in history.history.items():
        for team in teams:
            with open(
                    directory_path + "/" + str(base64.b64encode(team.name.encode(encoding="utf-8")), "utf-8"),
                    'x',
                    encoding="utf-8"
            ) as file:
                file.write(franchise.name)
