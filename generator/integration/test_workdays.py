from unittest import TestCase
from .workdays import WorkDays
from .dryg import DrygDAO


class TestGenerator(TestCase):
    def test_get_x_number_of_days_from_today_starts_with_the_next_day(self):
        w = WorkDays("2017-05-01", DummyClosedDaysDAO(), DummyDrygDAO())
        self.assertEqual("2017-05-02", w.next())

    def test_get_x_number_of_days_from_today_overflows_to_next_year(self):
        w = WorkDays("2017-12-29", DummyClosedDaysDAO(), DummyDrygDAO())
        self.assertEqual("2018-01-02", w.next())


class DummyClosedDaysDAO:
    def get_closed_days(self):
        return ["2017-07-17", "2017-07-18", "2017-07-19"]


class DummyDrygDAO(DrygDAO):
    def get_days_for_year(self, year):
        y = int(year)
        if y == 2017:
            return ["2017-05-01", "2017-05-02", "2017-12-29"]
        elif y == 2018:
            return ["2018-01-02"]
