from unittest import TestCase
from datetime import date

from generator.date_range import date_range


class TestDateRange(TestCase):

    def test_correct_range_is_generated_when_only_one_day(self):
        dates = list(date_range(date(2018, 12, 30), date(2018, 12, 31)))
        self.assertEquals(len(dates), 1)
        self.assertEquals(dates[0], date(2018, 12, 30))

    def test_correct_range_is_generated_when_multiple_days(self):
        dates = list(date_range(date(2018, 12, 28), date(2018, 12, 31)))
        self.assertEquals(len(dates), 3)
        self.assertEquals(dates[0], date(2018, 12, 28))
        self.assertEquals(dates[1], date(2018, 12, 29))
        self.assertEquals(dates[2], date(2018, 12, 30))
