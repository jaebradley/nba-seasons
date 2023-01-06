from __future__ import annotations

from html.parser import HTMLParser
from typing import Callable, Set

from .models import Season


class SeasonStartYearParser(HTMLParser):
    EXPECTED_ATTRIBUTES = {('scope', 'row'), ('class', 'left '), ('data-stat', 'season')}

    def __init__(self, start_year_consumer: Callable[[int], None]):
        super().__init__()
        self.start_year_consumer = start_year_consumer
        self.recording = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if "th" == tag and self.EXPECTED_ATTRIBUTES == set(attrs):
            self.recording += 1

    def handle_endtag(self, tag: str) -> None:
        if "th" == tag and 0 < self.recording:
            self.recording -= 1

    def handle_data(self, data: str) -> None:
        if 0 < self.recording:
            parts = data.split('-')
            if 2 != len(parts):
                raise ValueError("Expected two parts to season")

            self.start_year_consumer(int(parts[0]))


class SeasonChampionParser(HTMLParser):
    EXPECTED_ATTRIBUTES = {('class', 'left '), ('data-stat', 'champion')}

    def __init__(self, champion_consumer: Callable[[str], None]):
        super().__init__()
        self.champion_consumer = champion_consumer
        self.recording = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if "td" == tag and self.EXPECTED_ATTRIBUTES == set(attrs):
            self.recording += 1

    def handle_endtag(self, tag: str) -> None:
        if "td" == tag and 0 < self.recording:
            self.recording -= 1

    def handle_data(self, data: str) -> None:
        if 0 < self.recording:
            self.champion_consumer(data)


class SeasonLeagueParser(HTMLParser):
    EXPECTED_ATTRIBUTES = {('class', 'left '), ('data-stat', 'lg_id')}

    def __init__(self, consumer: Callable[[str], None]):
        super().__init__()
        self.consumer = consumer
        self.recording = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if "td" == tag and self.EXPECTED_ATTRIBUTES == set(attrs):
            self.recording += 1

    def handle_endtag(self, tag: str) -> None:
        if "td" == tag and 0 < self.recording:
            self.recording -= 1

    def handle_data(self, data: str) -> None:
        if 0 < self.recording:
            self.consumer(data)


def parse(html: str) -> Set[Season]:
    start_years = []
    champions = []
    leagues = []

    start_year_parser = SeasonStartYearParser(lambda value: start_years.append(value))
    start_year_parser.feed(html)
    start_year_parser.close()

    champion_parser = SeasonChampionParser(lambda value: champions.append(value))
    champion_parser.feed(html)
    champion_parser.close()

    league_parser = SeasonLeagueParser(lambda value: leagues.append(value))
    league_parser.feed(html)
    league_parser.close()

    if len(start_years) != len(champions) != len(leagues):
        raise ValueError("Length of start years and champions differs")

    return set(
        map(
            lambda values: Season(start_year=values[0], champion=values[1]),
            filter(
                lambda values: "NBA" in values[2],
                zip(start_years, champions, leagues)
            )
        )
    )
