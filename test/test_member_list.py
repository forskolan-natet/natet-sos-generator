from unittest import TestCase

from generator.model import MemberList


class TestMemberList(TestCase):
    def test_create_from_dicts(self):
        dict = {
            "id": 123,
            "first_name": "Kalle",
            "last_name": "Kanon",
            "sos_percentage": 50,
            "family": 42
        }
        dicts = [dict]

        members = MemberList.create_from_dicts(dicts)
        self.assertEqual(len(members), 1)
        m = members[0]
        self.assertEqual(m.id, dict.get("id"))
        self.assertEqual(m.first_name, dict.get("first_name"))
        self.assertEqual(m.last_name, dict.get("last_name"))
        self.assertEqual(m.sos_percentage, dict.get("sos_percentage"))
        self.assertEqual(m.family, dict.get("family"))
