from dataclasses import dataclass

from nba_seasons.models.math import NaturalNumber

"""
From https://en.wikipedia.org/wiki/ISO_8601#Years:
"ISO 8601 prescribes, as a minimum, a four-digit year [YYYY] to avoid the year 2000 problem. It therefore represents years from 0000 to 9999, year 0000 being equal to 1 BC and all others AD, similar to astronomical year numbering."
"""


@dataclass(frozen=True)
class Year(NaturalNumber):
    pass


@dataclass(frozen=True)
class YearDuration(NaturalNumber):
    pass
