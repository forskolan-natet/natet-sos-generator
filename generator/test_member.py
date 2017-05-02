from unittest import TestCase

from generator.models.member import Member


class TestMember(TestCase):

    def test_name(self):
        m = Member()
        m.first_name = 'Lisa'
        m.last_name = 'Svensson'
        self.assertEqual(m.name, 'Lisa Svensson')
