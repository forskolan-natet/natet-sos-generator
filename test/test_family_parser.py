from unittest import TestCase

from generator import Member
from generator.model import MemberList


class TestFamilyParser(TestCase):

    def test_can_match_two_members_to_a_family(self):
        members = MemberList()
        members.extend([Member(id=1, partner_id=2),
                        Member(id=2, partner_id=1)])
        members._parse_families()
        self.assertEqual(members.get_by_id(1).family, members.get_by_id(2).family)

    def test_can_match_three_members_to_two_families(self):
        members = MemberList()
        members.extend([Member(id=1, partner_id=2),
                        Member(id=2, partner_id=1),
                        Member(id=3)])
        members._parse_families()
        self.assertEqual(members.get_by_id(1).family, members.get_by_id(2).family)
        self.assertNotEqual(members.get_by_id(1).family, members.get_by_id(3).family)

    def test_can_match_four_members_to_two_families(self):
        members = MemberList()
        members.extend([Member(id=1, partner_id=2),
                        Member(id=2, partner_id=1),
                        Member(id=3, partner_id=4),
                        Member(id=4, partner_id=3)])
        members._parse_families()
        self.assertEqual(members.get_by_id(1).family, members.get_by_id(2).family)
        self.assertEqual(members.get_by_id(3).family, members.get_by_id(4).family)
        self.assertNotEqual(members.get_by_id(1).family, members.get_by_id(3).family)

    def test_can_create_family_name(self):
        members = MemberList()
        members.extend([Member(id=1, partner_id=2, first_name="Adam", last_name="Adamsson"),
                        Member(id=2, partner_id=1, first_name="Bertil", last_name="Bertilsson")])
        members._parse_families()
        self.assertEqual(members.get_by_id(1).family_name, members.get_by_id(2).family_name)
        self.assertEqual(members.get_by_id(1).family_name, "Familjen Bertil Bertilsson & Adam Adamsson")
        self.assertEqual(members.get_by_id(1).family_name, "Familjen Bertil Bertilsson & Adam Adamsson")

    def test_can_create_family_name_with_only_one_member(self):
        members = MemberList()
        members.extend([Member(id=1, first_name="Adam", last_name="Adamsson")])
        members._parse_families()
        self.assertEqual(members.get_by_id(1).family_name, "Adam Adamsson")

    def test_can_parse_sponsor(self):
        members = MemberList()
        members.extend([Member(id=1, partner_id=2, sponsor_to_member=3),
                        Member(id=2, partner_id=1, sponsor_to_member=3),
                        Member(id=3, partner_id=4, sponsored_by_member=1),
                        Member(id=4, partner_id=3, sponsored_by_member=1)])
        members._parse_families()
        members._parse_sponsors()
        self.assertEqual(members.get_by_id(1).sponsor_for_family, members.get_by_id(2).sponsor_for_family)
        self.assertEqual(members.get_by_id(1).sponsor_for_family, members.get_by_id(3).family)
        self.assertEqual(members.get_by_id(1).sponsor_for_family, members.get_by_id(4).family)

        self.assertEqual(members.get_by_id(3).sponsored_by_family, members.get_by_id(1).family)
        self.assertEqual(members.get_by_id(4).sponsored_by_family, members.get_by_id(1).family)

    def test_get_family_name_by_family_id(self):
        members = MemberList()
        members.extend([Member(id=1, first_name="Adam", last_name="Adamsson")])
        members._parse_families()
        self.assertEqual(members.get_family_name_by_family_id(1), "Adam Adamsson")
