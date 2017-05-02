from unittest import TestCase

from .exceptions import NotPossibleToGenerateSosError
from .generator import Generator
from .models.member import Member


class TestGenerator(TestCase):

    def test_generator_proportion_100_gives_two_sos(self):
        m = Member()
        m.proportion = 100
        generator = Generator([m])
        generator._populate_pot()
        self.assertEqual(len(generator.pot), 2)

    def test_generator_proportion_50_gives_one_sos(self):
        m = Member()
        m.proportion = 50
        generator = Generator([m])
        generator._populate_pot()
        self.assertEqual(len(generator.pot), 1)

    def test_generator_proportion_0_gives_no_sos(self):
        m = Member()
        m.proportion = 0
        generator = Generator([m])
        self.assertEqual(len(generator.pot), 0)

    def test_list_is_random(self):
        names_ordered = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
        members = []
        for index, name in enumerate(names_ordered):
            members.append(Member(first_name=name, proportion=50, family=index))

        generator = Generator(members)
        generator.generate()
        names = ""
        for m in generator.sos_list:
            names += m.first_name
        self.assertNotEqual(names, names_ordered)

    # Förmodligen obsolet?
    def test_member_not_allowed_more_than_once_in_holy_period(self):
        m = Member()
        generator = Generator([m])
        generator.sos_list.append(m)
        self.assertTrue(generator.is_member_already_in_holy_period(m))

    def test_members_family_not_allowed_more_than_once_in_holy_period(self):
        m1 = Member(family=1)
        m2 = Member(family=1)
        generator = Generator([m1, m2])
        generator.sos_list = [m1]
        self.assertTrue(generator.is_members_family_in_holy_period(m2))

    def test_sponsor_is_on_same_day_as_sponsored(self):
        sponsor = Member(first_name="sponsor", proportion=50, family=100, sponsor_for_family=200)
        sponsored = Member(first_name="sponsored", proportion=50, family=200)

        members = self._large_list_of_members()
        members.extend([sponsor, sponsored])
        generator = Generator(members)

        generator.generate()
        sos_days = generator.sos_days
        was_found = False
        for day in sos_days:
            if sponsor in day.members:
                self.assertTrue(sponsored in day.members)
                was_found = True
        self.assertTrue(was_found)

    def test_sponsor_is_always_on_an_even_position_in_sos_list(self):
        sponsor = Member(first_name="sponsor", proportion=50, family=100, sponsor_for_family=200)
        sponsored = Member(first_name="sponsored", proportion=50, family=200)

        members = self._large_list_of_members()
        members.extend([sponsor, sponsored])
        generator = Generator(members)

        generator.generate()
        self.assertEqual(generator.sos_list.index(sponsor) % 2, 0)

    def test_generator_retries_if_deadlock_occurs(self):
        m1 = Member(family=1)
        m2 = Member(family=1)
        generator = Generator([m1, m2])
        with self.assertRaises(NotPossibleToGenerateSosError):
            generator.generate()
        self.assertEqual(generator.number_of_retries_done, 10)

    def test_sponsors_are_always_picked_first(self):
        sponsor = Member(first_name="sponsor", proportion=50, family=100, sponsor_for_family=200)
        sponsored = Member(first_name="sponsored", proportion=50, family=200)

        members = self._large_list_of_members()
        members.extend([sponsor, sponsored])
        generator = Generator(members)
        generator.generate()
        first_day = generator.sos_days[0]
        self.assertTrue(sponsor in first_day.members)
        self.assertTrue(sponsored in first_day.members)

    @staticmethod
    def _large_list_of_members():
        members = []
        for index, name in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ1234567890"):
            members.append(Member(first_name=name, proportion=50, family=index))
        return members