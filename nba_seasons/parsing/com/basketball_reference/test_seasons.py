from unittest import TestCase

from nba_seasons.parsing.com.basketball_reference.seasons import parse, Season


class Test(TestCase):
    def test_parse(self):
        self.assertEqual(
            {Season(start_year=2018, champion="Toronto Raptors")},
            parse('<tr ><th scope="row" class="left " data-stat="season" ><a '
                  'href="/leagues/NBA_2019.html">2018-19</a></th><td class="left " data-stat="lg_id" ><a '
                  'href="/leagues/NBA_2019.html">NBA</a></td><td class="left " data-stat="champion" ><a '
                  'href="/teams/TOR/2019.html">Toronto Raptors</a></td><td class="left " data-stat="mvp" ><a '
                  'href="/players/a/antetgi01.html">G. Antetokounmpo</a></td><td class="left " data-stat="roy" ><a '
                  'href="/players/d/doncilu01.html">L. Dončić</a></td><td class="left " data-stat="pts_leader_name" '
                  '><a href="/players/h/hardeja01.html">J. Harden</a>&nbsp;(2818)</td><td class="left " '
                  'data-stat="trb_leader_name" ><a href="/players/d/drumman01.html">A. Drummond</a>&nbsp;('
                  '1232)</td><td class="left " data-stat="ast_leader_name" ><a href="/players/w/westbru01.html">R. '
                  'Westbrook</a>&nbsp;(784)</td><td class="left " data-stat="ws_leader_name" ><a '
                  'href="/players/h/hardeja01.html">J. Harden</a>&nbsp;(15.2)</td></tr>')
        )
