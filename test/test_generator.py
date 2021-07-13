from unittest import TestCase

from generator.exceptions import NotPossibleToGenerateSosError
from generator.generator import Generator
from generator.model import Member
from generator.integration.mock import MockWorkDaysService, MockClosedDaysDAO, MockDrygDAO


class TestGenerator(TestCase):

    @property
    def _basic_mock_work_day_service(self):
        return MockWorkDaysService(start_after_date="2017-01-02",
                                   closed_days_dao=MockClosedDaysDAO(),
                                   dryg_dao=MockDrygDAO())

    @property
    def _large_list_of_members(self):
        members = []
        for index, name in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ1234567890"):
            members.append(Member(first_name=name, sos_percentage=50, family=index))
        return members

    def test_generator_proportion_100_gives_two_sos(self):
        m = Member()
        m.sos_percentage = 100
        generator = Generator([m], self._basic_mock_work_day_service)
        generator._populate_pot()
        self.assertEqual(len(generator.pot), 2)

    def test_generator_proportion_50_gives_one_sos(self):
        m = Member()
        m.sos_percentage = 50
        generator = Generator([m], self._basic_mock_work_day_service)
        generator._populate_pot()
        self.assertEqual(len(generator.pot), 1)

    def test_generator_proportion_0_gives_no_sos(self):
        m = Member()
        m.sos_percentage = 0
        generator = Generator([m], self._basic_mock_work_day_service)
        self.assertEqual(len(generator.pot), 0)

    def test_list_is_random(self):
        names_ordered = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
        members = []
        for index, name in enumerate(names_ordered):
            members.append(Member(first_name=name, sos_percentage=50, family=index))

        generator = Generator(members, self._basic_mock_work_day_service)
        generator.generate()
        names = ""
        for day in generator.sos_days:
            for m in day.members:
                names += m.first_name
        self.assertNotEqual(names, names_ordered)

    def test_members_family_not_allowed_more_than_once_in_holy_period(self):
        m1 = Member(family=1)
        m2 = Member(family=1)
        m3 = Member(family=1)
        generator = Generator([m1, m2, m3], self._basic_mock_work_day_service)
        generator.sos_days.append_member(m1)
        generator.sos_days.append_member(m2)
        self.assertTrue(generator._is_members_family_in_holy_period(m3))

    def test_sponsor_is_on_same_day_as_sponsored(self):
        sponsor = Member(first_name="sponsor", sos_percentage=50, family=100, sponsor_for_family=200)
        sponsored = Member(first_name="sponsored", sos_percentage=50, family=200, sponsored_by_family=100)

        members = self._large_list_of_members
        members.extend([sponsor, sponsored])
        generator = Generator(members, self._basic_mock_work_day_service)

        generator.generate()
        sos_days = generator.sos_days

        found_sponsor = False
        found_sponsored = False
        for day in sos_days:
            if sponsor in day.members:
                found_sponsor = True
            if sponsored in day.members:
                found_sponsored = True

        self.assertTrue(found_sponsor, "Sponsor not in list")
        self.assertTrue(found_sponsored, "Sponsored not in list")

        for day in sos_days:
            if sponsor in day.members or sponsored in day.members:
                self.assertListEqual(sorted(day.members), sorted([sponsor, sponsored]))
                return

        self.fail("Sponsor was not in list of days")

    def test_when_sponsor_has_only_50_percent_sos(self):
        for i in range(0, 10):  # This test is flaky so repeat it
            sponsor = Member(first_name="sponsor", sos_percentage=50, family=100, sponsor_for_family=200)
            sponsored = Member(first_name="sponsored", sos_percentage=100, family=200, sponsored_by_family=100)

            members = self._large_list_of_members
            members.extend([sponsor, sponsored])
            generator = Generator(members, self._basic_mock_work_day_service)

            generator.generate()
            sos_days = generator.sos_days

            found_sponsor = 0
            found_sponsored = 0
            for day in sos_days:
                if sponsor in day.members:
                    found_sponsor += 1
                if sponsored in day.members:
                    found_sponsored += 1

            self.assertEqual(found_sponsor, 1, "Sponsor should only have 1 SOS since they have 50% SOS")
            self.assertEqual(found_sponsored, 1, "Sponsored should only have 1 SOS since they need to be with sponsor")

    def test_generator_retries_if_deadlock_occurs(self):
        m1 = Member(family=1)
        m2 = Member(family=1)
        generator = Generator([m1, m2], self._basic_mock_work_day_service, number_of_retries=10)
        with self.assertRaises(NotPossibleToGenerateSosError):
            generator.generate()
        self.assertEqual(generator.number_of_retries_done, 10)

    def test_member_is_not_allowed_to_have_sos_in_end_grace_period(self):
        m1 = Member(sos_percentage=50, family=1)
        m2 = Member(sos_percentage=50, family=2)
        m3 = Member(sos_percentage=50, family=3, end_date="2017-01-03")
        generator = Generator([m1, m2, m3], self._basic_mock_work_day_service, holy_period_length=0)
        generator.sos_days.append_member(m1)
        generator.sos_days.append_member(m2)
        generator.sos_days.append_member(m3)
        self.assertFalse(m3 in generator.sos_days.members)

    def test_last_day_is_full(self):
        m = Member(sos_percentage=50, family=1)
        generator = Generator([m], self._basic_mock_work_day_service, holy_period_length=0)
        generator.generate()
        self.assertListEqual([], generator.sos_days)
