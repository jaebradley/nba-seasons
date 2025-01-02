from unittest import TestCase

from nba_seasons.calculators.python import calculate_class_attributes


class Example:
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar


class Test(TestCase):
    def test(self):
        self.assertSetEqual({"foo", "bar"}, calculate_class_attributes(Example(foo="foo", bar="bar")))
