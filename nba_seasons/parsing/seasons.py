from yaml import load, Loader


def parse_seasons(seasons_file_path):
    with open(seasons_file_path, 'r', encoding="utf-8") as file:
        # TODO: @jbradley switch to using event / parse
        data = load(file, Loader=Loader)
        most_recent_starting_year = data.get('most recent starting year')
        seasons = data.get('seasons')

        seasons_from_most_recent_to_least = reversed(seasons)
        current_starting_year = most_recent_starting_year
        current_end_year = None
        season_data = []
        for current_season in seasons_from_most_recent_to_least:
            # TODO: convert this to an object
            season_data.append({
                'start year': current_starting_year,
                'end year': current_end_year
            })
            current_starting_year -= (current_season.get('duration in years') + current_season.get('offset in years'))
            current_end_year = current_starting_year + current_season.get('duration in years')

        if len(set(season_data)) != len(season_data):
            raise ValueError("Duplicates exist")

        return reversed(season_data)
