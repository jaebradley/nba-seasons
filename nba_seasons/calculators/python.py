from typing import Set, Type


def calculate_class_attributes(class_obj: Type) -> Set[str]:
    return set(filter(lambda value: not callable(value),
                      map(lambda attribute: getattr(class_obj, attribute),
                          filter(lambda attribute: attribute[:2] != '__', class_obj.__dict__.keys()))))
