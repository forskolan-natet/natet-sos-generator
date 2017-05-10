import random

from .exceptions import DeadlockInGenerationError, NotPossibleToGenerateSosError
from .model import DayList
from .integration.workdays import WorkDaysService

DEFAULT_HOLY_PERIOD_LENGTH = 10
SPONSOR_DEFAULT_HOLY_PERIOD_LENGTH = 10
NUMBER_OF_RETRIES = 1000


class Generator:
    pot = []
    sos_days = None

    def __init__(self, members, work_days_service: WorkDaysService,
                 holy_period_length=DEFAULT_HOLY_PERIOD_LENGTH,
                 sponsor_holy_period_length=SPONSOR_DEFAULT_HOLY_PERIOD_LENGTH):
        self.holy_period_length = holy_period_length
        self.sponsor_holy_period_length = sponsor_holy_period_length
        self.members = members
        self.number_of_retries_done = 0
        self.work_days_service = work_days_service
        self._populate_pot()

    def _populate_pot(self):
        self.pot = []
        self.work_days_service.reset()
        self.sos_days = DayList(work_days_service=self.work_days_service)
        for member in self.members:
            if member.sos_percentage == 100:
                self.pot.extend([member, member])
            elif member.sos_percentage == 50:
                self.pot.append(member)

    def generate(self):
        while self.number_of_retries_done < NUMBER_OF_RETRIES:
            try:
                self._populate_pot()
                self.__generate()
                return
            except DeadlockInGenerationError:
                self.number_of_retries_done += 1
        raise NotPossibleToGenerateSosError

    def __generate(self):
        while self.pot:
            member = self._get_next_member_from_pot()
            self.__move_from_pot_to_sos_list(member)

            if member.is_sponsor:
                sponsored_family = member.sponsor_for_family
                sponsored_family_members = [x for x in self.pot if x.family == sponsored_family]
                if sponsored_family_members:
                    first_sponsored_family_member = sponsored_family_members[0]
                    self.__move_from_pot_to_sos_list(first_sponsored_family_member)

        if not self.sos_days[-1].is_full:
            self.sos_days.pop()

    def __move_from_pot_to_sos_list(self, member):
        self.pot.remove(member)
        self.sos_days.append_member(member)

    def _get_next_member_from_pot(self):
        good_pot = list(self.pot)
        bad_pot = []
        while good_pot:
            next_member = None

            if self.__is_new_day():
                sponsors = [x for x in good_pot if x.is_sponsor]
                if sponsors:
                    next_member = sponsors[0]

            if next_member is None:
                next_member = random.choice(good_pot)

            if self._is_members_family_in_holy_period(next_member) \
                    or self._is_sponsored_and_sponsor_is_in_pot(next_member) \
                    or self._is_sponsors_family_in_sponsor_holy_period_length(next_member):
                good_pot.remove(next_member)
                bad_pot.append(next_member)
                continue

            return next_member

        raise DeadlockInGenerationError

    def __is_new_day(self):
        if self.sos_days:
            return self.sos_days[-1].is_full
        return True

    def _get_holy_period(self):
        length = len(self.sos_days)
        holy_period_start = \
            0 if length < self.holy_period_length \
            else length - self.holy_period_length
        return self.sos_days[holy_period_start:]

    def _is_members_family_in_holy_period(self, member):
        return self.is_member_in_period(member, self._get_holy_period())

    def _get_sponsor_holy_period(self):
        length = len(self.sos_days)
        holy_period_start = length - self.sponsor_holy_period_length
        holy_period_start = 0 if holy_period_start < 0 else holy_period_start
        return self.sos_days[holy_period_start:]

    def _is_sponsors_family_in_sponsor_holy_period_length(self, member):
        if not member.is_sponsor:
            return False
        return self.is_member_in_period(member, self._get_sponsor_holy_period())

    @staticmethod
    def is_member_in_period(member, period):
        for day in period:
            if day.contains_family(member.family):
                return True
        return False

    def _is_sponsored_and_sponsor_is_in_pot(self, member):
        if member.is_sponsored and [x for x in self.pot if x.sponsor_for_family == member.family]:
            return True
        return False
