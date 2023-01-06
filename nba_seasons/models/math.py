from dataclasses import dataclass


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
