from collections import OrderedDict

from .models import League


class LeagueWriter:

    def __init__(self, output_directory_path):
        self.output_directory_path = output_directory_path

    def write(self, league: League):
        with open(self.output_directory_path + "/" + league.name + ".yaml", 'w', encoding="utf-8") as output_file:
            output_file.write("starting year: " + str(league.start_year) + "\n")
            output_file.write("seasons: \n")
            current_season = league.inaugural_season
            while current_season is not None:
                output_file.write("  - offset in years: " + str(current_season.offset_in_years) + "\n")
                output_file.write("    duration in years: " + str(current_season.duration_in_years) + "\n")
                output_file.write("    team name by franchise names: \n")

                for franchise_name, team_name in OrderedDict(
                        sorted(current_season.team_name_by_franchise_names.items())).items():
                    output_file.write("      " + franchise_name + ": " + team_name + "\n")

                current_season = current_season.next_season
