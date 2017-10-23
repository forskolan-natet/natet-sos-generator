from unittest import TestCase
from unittest import skip
from generator.integration.database import *


class TestScheduleLiveDAO(TestCase):
    @skip
    def test_get_last_scheduled_date(self):
        dao = ScheduleLiveDAO()
        print(dao.get_last_scheduled_date())

    @skip
    def test_group_names(self):
        dao = GroupDAO()
        print(dao.get_groups())
