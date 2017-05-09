from unittest import TestCase

from . import workdays


class TestGenerator(TestCase):

    def setUp(self):
        self.dates = workdays.get_for_year(2017)

    def test_2017_has_251_workdays(self):
        self.assertEqual(len(self.dates), 251)

    def test_that_2017_05_01_is_not_a_workday(self):
        self.assertFalse("2017-05-01" in self.dates)

    def test_that_2017_05_02_is_a_workday(self):
        self.assertTrue("2017-05-02" in self.dates)

    def test_get_x_number_of_days_from_today_starts_with_the_next_day(self):
        work_days = workdays.get_x_number_of_days_from_date(10, '2017-01-02')
        self.assertEqual("2017-01-03", work_days[0])

    def test_get_x_number_of_days_from_today_overflows_to_next_year(self):
        work_days = workdays.get_x_number_of_days_from_date(100, '2017-12-29')
        self.assertTrue("2018-01-02" in work_days)
