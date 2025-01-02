from typing import Dict

from yaml import load, Loader


class EnumWriter:
    def __init__(
            self,
            element_generator,
            less_than_method_generator,
            greater_than_method_generator,
            element_property_name_generator,
            init_generator,
            enum_element_map_generator,
            static_constructor_generator
    ):
        self.less_than_method_generator = less_than_method_generator
        self.greater_than_method_generator = greater_than_method_generator
        self.element_generator = element_generator
        self.element_property_name_generator = element_property_name_generator
        self.init_generator = init_generator
        self.enum_element_map_generator = enum_element_map_generator
        self.static_constructor_generator = static_constructor_generator

    def generate(self, name, elements, lt_properties, gt_properties, value_consumer) -> Dict[str, str]:
        value = ""
        value += "from enum import Enum, auto\n"
        value += "class " + name + "(Enum):\n"
        property_names = self.element_property_name_generator.generate(class_obj=elements[0]._class_)
        value += self.init_generator(property_names=property_names)
        value += map(lambda element: self.element_generator.generate(element=element), elements)
        value += self.less_than_method_generator.generate(properties=lt_properties)
        value += self.greater_than_method_generator.generate(properties=gt_properties)
        property_mappings = map(lambda p: self.enum_element_map_generator.generate(property=p),
                                property_names)
        # for prop in properties:
        #     property_mapping = self.enum_element_map_generator.generate(property=prop)
        #     value += self.static_constructor_generator.generate(property_name=prop,
        #                                                         property_mapping_name=property_mapping.name)
        #
        #     for property_mapping in property_mappings:
        #         value += self.static_constructor_generator.generate(property_name=property_mapping.property,
        #                                                             property_mapping_name=property_mapping.name)
        #
        # for property_mapping in property_mappings:
        #     value += property_mapping.value

        value_consumer.consume(value)


def generate_client(file_path, output_file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        # TODO: @jbradley switch to using event / parse
        data = load(file, Loader=Loader)
        most_recent_starting_year = data.get('most recent starting year')
        seasons = data.get('seasons')

        seasons_from_most_recent_to_least = reversed(seasons)
        current_starting_year = most_recent_starting_year
        season_data = []
        for current_season in seasons_from_most_recent_to_least:
            season_data.append({
                'start year': current_starting_year
            })
            current_starting_year -= (current_season.get('duration in years') + current_season.get('offset in years'))

    with open("/Users/jaebradley/projects/nba-seasons/nba_seasons/output/clients/python/test.py", 'w',
              encoding="utf-8") as output_file:
        output_file.write("from enum import Enum, auto\n")
        output_file.write("class Season(Enum):\n")

        for season in reversed(season_data):
            output_file.write(
                "    _" + str(season.get('start year')) + " = " + "(auto(), " + str(season.get("start year")) + ")\n")

        output_file.write(
            """
    def __init__(self, value, start_year):
        self._value_ = value
        self._start_year_ = start_year

    @property
    def start_year(self):
        return self._start_year_

    def __lt__(self, other):
        return self.start_year < other.start_year

    def __gt__(self, other):
        return self.start_year > other.start_year

    def __str__(self) -> str:
        return self.name
            """
        )
