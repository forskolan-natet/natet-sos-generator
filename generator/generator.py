import random

from .constants import GRANEN_ID, TALLEN_ID
from .exceptions import BadDistributionBetweenDepartmentsError, DeadlockInGenerationError, DepartmentNotAvailableError,\
    NotPossibleToGenerateSosError
from .model import DayList
from .integration.workdays import WorkDaysService

DEFAULT_HOLY_PERIOD_LENGTH = 11
DEFAULT_MAX_NUMBER_OF_RETRIES = 100000


class Generator:
    pot = []
    sos_days = None
    _lowest_bad_count = None
    _lowest_bad_count_sos_days = None

    def __init__(self, members, work_days_service: WorkDaysService,
                 holy_period_length=DEFAULT_HOLY_PERIOD_LENGTH, number_of_retries=DEFAULT_MAX_NUMBER_OF_RETRIES,
                 last_ten_days=[]):
        self.holy_period_length = holy_period_length
        self.members = members
        self.number_of_retries_done = 0
        self.work_days_service = work_days_service
        self.number_of_retries = number_of_retries
        self.last_ten_days = last_ten_days
        self._populate_pot()

    def _populate_pot(self):
        self.pot = []
        self.work_days_service.reset()
        self.sos_days = DayList(work_days_service=self.work_days_service)
        for member in self.members:
            if member.sos_percentage == 150:
                self.pot.extend([member, member, member])
            elif member.sos_percentage == 100:
                self.pot.extend([member, member])
            elif member.sos_percentage == 50:
                self.pot.append(member)

    def generate(self):
        one_thousandth = self.number_of_retries / 1000
        while self.number_of_retries_done < self.number_of_retries and self._lowest_bad_count != 0:
            try:
                self._populate_pot()
                self.__generate()
            except (BadDistributionBetweenDepartmentsError, DeadlockInGenerationError, DepartmentNotAvailableError):
                self.number_of_retries_done += 1

            if self.number_of_retries_done % one_thousandth == 0:
                print("%s%% with lowest_bad_count at %s" % (self.number_of_retries_done / (one_thousandth * 10),
                                                            self._lowest_bad_count))

        if self._lowest_bad_count_sos_days is None:
            raise NotPossibleToGenerateSosError
        else:
            self.sos_days = self._lowest_bad_count_sos_days
            return

    def __generate(self):
        while self.pot:
            member = self._get_next_member_from_pot()

            if member.is_sponsor:
                sponsored_family = member.sponsor_for_family
                sponsored_family_members = [x for x in self.pot if x.family == sponsored_family]
                if sponsored_family_members:
                    first_sponsored_family_member = sponsored_family_members[0]
                    self.__move_from_pot_to_sos_list(first_sponsored_family_member)

                if member.sos_percentage < 100:
                    next_sponsored_family_member = sponsored_family_members[-1]
                    if next_sponsored_family_member in self.pot:
                        self.pot.remove(next_sponsored_family_member)

        self.__remove_last_day_if_both_depatments_do_not_have_a_cleaner()

        for day in self.sos_days:
            if day.tallen.is_sponsor and day.tallen.sponsor_for_family != day.granen.family \
                    or day.granen.is_sponsor and day.granen.sponsor_for_family != day.tallen.family:
                raise DeadlockInGenerationError

        sos_per_family = {}
        for day in self.sos_days:
            family = day.tallen.family
            if not sos_per_family.get(family):
                sos_per_family[family] = {"tallen": 0, "granen": 0}

            sos_per_family[family]["tallen"] = sos_per_family[family]["tallen"] + 1

            family = day.granen.family
            if not sos_per_family.get(family):
                sos_per_family[family] = {"tallen": 0, "granen": 0}

            sos_per_family[family]["granen"] = sos_per_family[family]["granen"] + 1

        bad_count = 0
        for family, sos_count_per_department in sos_per_family.items():
            total_number_of_sos = sos_count_per_department["tallen"] + sos_count_per_department["granen"]
            diff_between_dapartments = abs(sos_count_per_department["tallen"] - sos_count_per_department["granen"])

            if total_number_of_sos == 4 and diff_between_dapartments >= 4 \
                    or total_number_of_sos == 3 and diff_between_dapartments >= 3 \
                    or total_number_of_sos == 2 and diff_between_dapartments >= 2:
                raise BadDistributionBetweenDepartmentsError

            if total_number_of_sos % 2 == 0 and diff_between_dapartments > 0:
                bad_count += diff_between_dapartments
            elif total_number_of_sos % 2 == 1 and diff_between_dapartments > 1:
                bad_count += diff_between_dapartments - 1

        if self._lowest_bad_count is None or bad_count < self._lowest_bad_count:
            self._lowest_bad_count = bad_count
            self._lowest_bad_count_sos_days = self.sos_days

    def __move_from_pot_to_sos_list(self, member):
        family = member.family
        tallen_count = 0
        granen_count = 0
        for day in self.sos_days:
            if day.tallen and day.tallen.family == family:
                tallen_count += 1
            if day.granen and day.granen.family == family:
                granen_count += 1

        department = None
        if tallen_count < granen_count:
            department = TALLEN_ID
        elif granen_count < tallen_count:
            department = GRANEN_ID

        self.sos_days.append_member(member, department)
        self.pot.remove(member)

    def _get_next_member_from_pot(self):
        good_pot = list(self.pot)
        bad_pot = []
        while good_pot:
            next_member = random.choice(good_pot)
            if self._is_members_family_in_holy_period(next_member) \
                    or self._is_sponsored_and_sponsor_is_in_pot(next_member) \
                    or next_member.is_sponsor and not self._must_create_new_day_in_sos_list():
                good_pot.remove(next_member)
                bad_pot.append(next_member)
                continue

            try:
                self.__move_from_pot_to_sos_list(next_member)
                return next_member
            except DepartmentNotAvailableError:
                good_pot.remove(next_member)
                bad_pot.append(next_member)
                continue

        raise DeadlockInGenerationError

    def _must_create_new_day_in_sos_list(self):
        if self.sos_days:
            return self.sos_days[-1].is_full
        return True

    def _get_holy_period(self):
        complete_period = self.last_ten_days + self.sos_days
        length = len(complete_period)
        holy_period_start = \
            0 if length < self.holy_period_length \
                else length - self.holy_period_length
        return complete_period[holy_period_start:]

    def _is_members_family_in_holy_period(self, member):
        return self.is_member_in_period(member, self._get_holy_period())

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

    def __remove_last_day_if_both_depatments_do_not_have_a_cleaner(self):
        if not self.sos_days[-1].is_full:
            self.sos_days.pop()
