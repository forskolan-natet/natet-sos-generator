import random

from .exceptions import DeadlockInGenerationError, NotPossibleToGenerateSosError
from .models.day import Day

# Why 9? A regular week has 5 days á 2 SoS members.
# If you/your family is not present in the last 9 positions you will not have two SoS in the same week.
DEFAULT_HOLY_PERIOD_LENGTH = 9

NUMBER_OF_TRIES_TO_GENERATE = 10


class Generator:

    def __init__(self, members, holy_period_length=DEFAULT_HOLY_PERIOD_LENGTH):
        self.members = members
        self.pot = []
        self.sos_list = []
        self.holy_period_length = holy_period_length
        self.sos_days = []
        self.number_of_retries_done = 0

        #self.__populate_pot()

    def _populate_pot(self):
        for member in self.members:
            if member.proportion == 100:
                self.pot.extend([member, member])
            elif member.proportion == 50:
                self.pot.append(member)

    def generate(self):
        for x in range(0, NUMBER_OF_TRIES_TO_GENERATE):
            try:
                self._populate_pot()
                self.__generate()
                return
            except DeadlockInGenerationError:
                self.number_of_retries_done += 1
        raise NotPossibleToGenerateSosError

    def __generate(self):
        while self.pot:
            member = self.get_next_member_from_pot()
            if member is None:
                raise DeadlockInGenerationError

            self.__move_from_pot_to_sos_list(member)

            if member.is_sponsor:
                sponsored_family = member.sponsor_for_family
                sponsored_family_members = [x for x in self.pot if x.family == sponsored_family]
                if sponsored_family_members:
                    first_sponsored_family_member = sponsored_family_members[0]
                    self.__move_from_pot_to_sos_list(first_sponsored_family_member)

        for member1, member2 in zip(self.sos_list[0::2], self.sos_list[1::2]):
            self.sos_days.append(Day([member1, member2]))

    def __move_from_pot_to_sos_list(self, member):
        self.pot.remove(member)
        self.sos_list.append(member)

    def get_next_member_from_pot(self):
        good_pot = list(self.pot)
        bad_pot = []
        while good_pot:
            next_member = None

            if self._is_new_day():
                sponsors = [x for x in good_pot if x.is_sponsor]
                if sponsors:
                    next_member = sponsors[0]

            if next_member is None:
                next_member = random.choice(good_pot)

            if self.is_member_already_in_holy_period(next_member) \
                    or self.is_members_family_in_holy_period(next_member):
                good_pot.remove(next_member)
                bad_pot.append(next_member)
                continue

            return next_member

    def _is_new_day(self):
        return len(self.sos_list) % 2 == 0

    def _get_holy_period_members(self):
        length = len(self.sos_list)
        holy_period_start = length - self.holy_period_length
        holy_period_start = 0 if holy_period_start < 0 else holy_period_start
        return self.sos_list[holy_period_start:]

    def is_member_already_in_holy_period(self, member):
        holy_period_mebers = self._get_holy_period_members()
        return holy_period_mebers.count(member) > 0

    def is_members_family_in_holy_period(self, member):
        holy_period_mebers = self._get_holy_period_members()
        for o in self.members:
            if o.family == member.family:
                if o in holy_period_mebers:
                    return True
        return False
