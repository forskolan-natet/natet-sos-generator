from unittest import TestCase
from generator.integration.workdays import WorkDaysService
from generator.integration.mock import MockClosedDaysDAO, MockDrygDAO


class TestWorkDaysService(TestCase):
    def test_get_x_number_of_days_from_today_starts_with_the_next_day(self):
        w = WorkDaysService("2017-05-02", MockClosedDaysDAO(), MockDrygDAO())
        self.assertEqual("2017-05-03", w.next())

    def test_get_x_number_of_days_from_today_overflows_to_next_year(self):
        w = WorkDaysService("2017-12-29", MockClosedDaysDAO(), MockDrygDAO())
        self.assertEqual("2018-01-02", w.next())
