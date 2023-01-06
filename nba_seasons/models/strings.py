from dataclasses import dataclass


@dataclass(frozen=True)
class NonEmptyString:
    value: str

    def __post_init__(self):
        if 0 >= len(self.value):
            raise ValueError("String cannot be empty")
