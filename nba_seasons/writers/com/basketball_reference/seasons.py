from collections import OrderedDict

from nba_seasons.models.basketball_reference import League


class LeagueWriter:

    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path

    def write(self, league: League):
        with open(self.output_directory_path + "/" + league.name.value + ".yaml", 'w', encoding="utf-8") as output_file:
            output_file.write("most recent starting year: " + str(league.most_recent_season[0].value) + "\n")
            output_file.write("seasons: \n")
            for current_season in reversed(list(league.most_recent_season[1])):
                output_file.write("  - offset in years: " + str(current_season.offset.value) + "\n")
                output_file.write("    duration in years: " + str(current_season.duration.value) + "\n")
                output_file.write("    team name by franchise names: \n")

                for franchise_name, team_name in OrderedDict(
                        sorted(current_season.team_name_by_franchise_names.items(),
                               key=lambda entry: entry[0].value)).items():
                    output_file.write("      " + franchise_name.value + ": " + team_name.value + "\n")
