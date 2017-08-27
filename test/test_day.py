from unittest import TestCase

from generator.model import Day, Member


class TestDay(TestCase):

    def test_tallen_property_is_None_when_no_members(self):
        d = Day("2017-01-01", [])
        self.assertIsNone(d.tallen)

    def test_tallen_property_is_set_when_day_has_one_member(self):
        d = Day("2017-01-01", [Member()])
        self.assertIsNotNone(d.tallen)

    def test_tallen_property_is_set_when_day_has_two_members(self):
        d = Day("2017-01-01", [Member(), Member()])
        self.assertIsNotNone(d.tallen)
