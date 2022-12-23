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


@dataclass(frozen=True, eq=True)
class League:
    name: str
    start_year: int
    inaugural_season: Season
