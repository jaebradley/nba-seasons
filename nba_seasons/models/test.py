from enum import Enum, auto


class Season(Enum):
    FIRST = (auto(), 1)
    SECOND = (auto(), 2)
    THIRD = (auto(), 3)

    def __init__(self, value, start_year):
        self._value_ = value
        self._start_year_ = start_year

    @property
    def start_year(self):
        return self._start_year_

    def __lt__(self, other):
        return self.start_year < other.start_year

    def __gt__(self, other):
        return self.start_year > other.start_year

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_start_year(start_year):
        return SEASON_BY_START_YEAR.get(start_year)

Season._st


SEASON_BY_START_YEAR = {
    1: Season.FIRST,
    2: Season.SECOND,
    3: Season.THIRD
}
