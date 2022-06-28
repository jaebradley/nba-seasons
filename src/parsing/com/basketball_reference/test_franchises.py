from unittest import TestCase

from franchises import FranchiseAndTeamParser, Record


class TestFranchiseAndTeamParser(TestCase):
    def test_parse_franchise(self):
        parsed_values = set()
        parser = FranchiseAndTeamParser(consumer=lambda record: parsed_values.add(record))
        parser.feed(
            '<tr class="full_table" ><th scope="row" class="left " data-stat="franch_name" ><a '
            'href="/teams/ATL/">Atlanta Hawks</a></th><td class="left " data-stat="lg_id" >NBA</td><td class="right " '
            'data-stat="year_min" >1949-50</td><td class="right " data-stat="year_max" >2021-22</td><td class="right '
            '" data-stat="years" >73</td><td class="right " data-stat="g" >5773</td><td class="right " '
            'data-stat="wins" >2850</td><td class="right " data-stat="losses" >2923</td><td class="right " '
            'data-stat="win_loss_pct" >.494</td><td class="right " data-stat="years_playoffs" >48</td><td '
            'class="right " data-stat="years_division_champion" >12</td><td class="right iz" '
            'data-stat="years_conference_champion" >0</td><td class="right " data-stat="years_league_champion" '
            '>1</td></tr>')
        parser.close()

        self.assertSetEqual(
            {
                Record(
                    name="Atlanta Hawks",
                    type=Record.Type.FRANCHISE,
                    league_name="NBA",
                    first_season_start_year="1949-50",
                    last_season_start_year="2021-22"
                )
            },
            parsed_values
        )

    def test_parse_team(self):
        parsed_values = set()
        parser = FranchiseAndTeamParser(consumer=lambda record: parsed_values.add(record))
        parser.feed(
            '<tr class="partial_table" ><th scope="row" class="right " data-stat="team_name" >Atlanta Hawks</th><td '
            'class="left " data-stat="lg_id" >NBA</td><td class="right " data-stat="year_min" >1968-69</td><td '
            'class="right " data-stat="year_max" >2021-22</td><td class="right " data-stat="years" >54</td><td '
            'class="right " data-stat="g" >4355</td><td class="right " data-stat="wins" >2152</td><td class="right " '
            'data-stat="losses" >2203</td><td class="right " data-stat="win_loss_pct" >.494</td><td class="right " '
            'data-stat="years_playoffs" >35</td><td class="right " data-stat="years_division_champion" >6</td><td '
            'class="right iz" data-stat="years_conference_champion" >0</td><td class="right iz" '
            'data-stat="years_league_champion" >0</td></tr>')
        parser.close()

        self.assertSetEqual(
            {
                Record(
                    name="Atlanta Hawks",
                    type=Record.Type.TEAM,
                    league_name="NBA",
                    first_season_start_year="1968-69",
                    last_season_start_year="2021-22"
                )
            },
            parsed_values
        )

    def test_parse_franchise_and_team(self):
        parsed_values = set()
        parser = FranchiseAndTeamParser(consumer=lambda record: parsed_values.add(record))
        parser.feed('<tr class="full_table" ><th scope="row" class="left " data-stat="franch_name" ><a '
                    'href="/teams/ATL/">Atlanta Hawks</a></th><td class="left " data-stat="lg_id" >NBA</td><td '
                    'class="right " data-stat="year_min" >1949-50</td><td class="right " data-stat="year_max" '
                    '>2021-22</td><td class="right " data-stat="years" >73</td><td class="right " data-stat="g" '
                    '>5773</td><td class="right " data-stat="wins" >2850</td><td class="right " data-stat="losses" '
                    '>2923</td><td class="right " data-stat="win_loss_pct" >.494</td><td class="right " '
                    'data-stat="years_playoffs" >48</td><td class="right " data-stat="years_division_champion" '
                    '>12</td><td class="right iz" data-stat="years_conference_champion" >0</td><td class="right " '
                    'data-stat="years_league_champion" >1</td></tr><tr class="partial_table" ><th scope="row" '
                    'class="right " data-stat="team_name" >Atlanta Hawks</th><td class="left " data-stat="lg_id" '
                    '>NBA</td><td class="right " data-stat="year_min" >1968-69</td><td class="right " '
                    'data-stat="year_max" >2021-22</td><td class="right " data-stat="years" >54</td><td class="right '
                    '" data-stat="g" >4355</td><td class="right " data-stat="wins" >2152</td><td class="right " '
                    'data-stat="losses" >2203</td><td class="right " data-stat="win_loss_pct" >.494</td><td '
                    'class="right " data-stat="years_playoffs" >35</td><td class="right " '
                    'data-stat="years_division_champion" >6</td><td class="right iz" '
                    'data-stat="years_conference_champion" >0</td><td class="right iz" '
                    'data-stat="years_league_champion" >0</td></tr>')
        parser.close()

        self.assertSetEqual(
            {
                Record(
                    name="Atlanta Hawks",
                    type=Record.Type.FRANCHISE,
                    league_name="NBA",
                    first_season_start_year="1949-50",
                    last_season_start_year="2021-22"
                ),
                Record(
                    name="Atlanta Hawks",
                    type=Record.Type.TEAM,
                    league_name="NBA",
                    first_season_start_year="1968-69",
                    last_season_start_year="2021-22"
                )
            },
            parsed_values
        )

    def test_parse_defunct_franchise(self):
        parsed_values = set()
        parser = FranchiseAndTeamParser(consumer=lambda record: parsed_values.add(record))
        parser.feed('<tr class="full_table" ><th scope="row" class="left " data-stat="franch_name" ><a '
                    'href="/teams/AND/">Anderson Packers</a></th><td class="left " data-stat="lg_id" >NBA</td><td '
                    'class="right " data-stat="year_min" >1949-50</td><td class="right " data-stat="year_max" '
                    '>1949-50</td><td class="right " data-stat="years" >1</td><td class="right " data-stat="g" '
                    '>64</td><td class="right " data-stat="wins" >37</td><td class="right " data-stat="losses" '
                    '>27</td><td class="right " data-stat="win_loss_pct" >.578</td><td class="right " '
                    'data-stat="years_playoffs" >1</td><td class="right iz" data-stat="years_division_champion" '
                    '>0</td><td class="right iz" data-stat="years_conference_champion" >0</td><td class="right iz" '
                    'data-stat="years_league_champion" >0</td></tr>')
        parser.close()

        self.assertSetEqual(
            {
                Record(
                    name="Anderson Packers",
                    type=Record.Type.FRANCHISE,
                    league_name="NBA",
                    first_season_start_year="1949-50",
                    last_season_start_year="1949-50"
                )
            },
            parsed_values
        )
