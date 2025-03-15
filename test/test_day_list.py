from unittest import TestCase
from datetime import datetime

from generator.model import Day, DayList, Member
from generator.integration.mock import MockWorkDaysService, MockClosedDaysDAO, MockDrygDAO


class TestDayList(TestCase):

    def test_append_member_when_list_is_empty(self):
        dl = DayList(work_days_service=MockWorkDaysService(start_after_date="2017-01-02",
                                                           closed_days_dao=MockClosedDaysDAO(""),
                                                           dryg_dao=MockDrygDAO()))
        m = Member(first_name="Kalle", last_name="Kula")
        dl.append_member(m)
        self.assertTrue(m in dl[0].members)

    def test_member_is_allowed_on_day_when_no_end_date_is_set(self):
        member = Member(end_date=None)
        day = Day("2017-01-01")
        self.assertFalse(DayList.is_day_within_members_end_grace_period(member=member, day=day))

    def test_member_is_allowed_on_day_when_end_date_is_outside_grace_period(self):
        member = Member(end_date="2017-02-15")
        day = Day("2017-01-01")
        self.assertFalse(DayList.is_day_within_members_end_grace_period(member=member, day=day))

    def test_member_is_not_allowed_on_day_when_end_date_is_within_grace_period(self):
        member = Member(end_date="2017-01-15")
        day = Day("2017-01-01")
        self.assertTrue(DayList.is_day_within_members_end_grace_period(member=member, day=day))

    def test_prev_month(self):
        self.assertEqual("2017-01-01", self._prev_month("2017-02-01"))
        self.assertEqual("2016-12-01", self._prev_month("2017-01-01"))
        self.assertEqual("2016-01-29", self._prev_month("2016-02-29"))
        self.assertEqual("2016-02-29", self._prev_month("2016-03-29"))
        self.assertEqual("2016-02-29", self._prev_month("2016-03-31"))

    def _prev_month(self, date):
        date = datetime.strptime(date, "%Y-%m-%d").date()
        prev_month_date = DayList.prev_month(date)
        return str(prev_month_date)