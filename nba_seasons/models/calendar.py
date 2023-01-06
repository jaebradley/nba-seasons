from dataclasses import dataclass

from nba_seasons.models.math import PositiveInteger, NaturalNumber


@dataclass(frozen=True)
class GregorianCalendarCommonEraYearCount(PositiveInteger):
    pass


@dataclass(frozen=True)
class GregorianCalendarYearDuration(NaturalNumber):
    pass
