from unittest import TestCase
from datetime import datetime

from generator.model import Member


class TestMember(TestCase):
    def test_name(self):
        m = Member()
        m.first_name = 'Lisa'
        m.last_name = 'Svensson'
        self.assertEqual(m.name, 'Lisa Svensson')

    def test_create_from_dict(self):
        dict = {
            "id": 123,
            "first_name": "Kalle",
            "last_name": "Kanon",
            "sos_percentage": 50,
            "family": 42,
            "end_date": "2018-01-01"
        }
        m = Member(**dict)
        self.assertEqual(m.id, dict.get("id"))
        self.assertEqual(m.first_name, dict.get("first_name"))
        self.assertEqual(m.last_name, dict.get("last_name"))
        self.assertEqual(m.sos_percentage, dict.get("sos_percentage"))
        self.assertEqual(m.family, dict.get("family"))
        self.assertEqual(m.end_date, datetime.strptime(dict.get("end_date"), "%Y-%m-%d").date())
