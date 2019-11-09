import random
from datetime import datetime

from .exceptions import DepartmentNotAvailableError, TooManyMembersOnDayError
from .constants import GRANEN_ID, TALLEN_ID


today = datetime.now().date()


class Member:
    def __init__(self, id=0, first_name="", last_name="", sos_percentage=100, family=0, sponsor_for_family=None,
                 sponsored_by_family=None, end_date=None, start_date=None, partner_id=None, sponsored_by_member=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sos_percentage = sos_percentage
        self.family = family
        self.sponsor_for_family = sponsor_for_family
        self.sponsored_by_family = sponsored_by_family
        self.start_date = start_date
        self.sponsored_by_member = sponsored_by_member
        self.partner_id = partner_id
        self.family_name = None
        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            self.end_date = end_date

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def is_sponsor(self):
        return self.sponsor_for_family is not None

    @property
    def is_sponsored(self):
        return self.sponsored_by_family is not None

    def __repr__(self):
        return "<%s>" % self.name


class MemberList(list):
    @staticmethod
    def create_from_dicts(dicts):
        members = MemberList()
        for m in dicts:
            members.append(Member(**m))

        members._parse_families()
        members._parse_sponsors()
        return members

    def _parse_families(self):
        family_id = 0
        members_dict = self.__members_by_id()
        new_members_list = []

        while len(members_dict) > 0:
            family_id += 1
            member1 = members_dict.popitem()[1]
            member1.family = family_id
            new_members_list.append(member1)
            family_name = '%s %s' % (member1.first_name, member1.last_name)
            if member1.partner_id:
                member2 = members_dict.pop(member1.partner_id)
                member2.family = family_id
                new_members_list.append(member2)
                family_name = "Familjen %s & %s %s" % (family_name, member2.first_name, member2.last_name)
                member2.family_name = family_name
            member1.family_name = family_name

    def _parse_sponsors(self):
        for member in self:
            if member.sponsored_by_member:
                if MemberList.__is_within_sponsor_period(member):
                    sponsor = self.get_by_id(member.sponsored_by_member)
                    member.sponsored_by_family = sponsor.family
                    if member.partner_id is not None:
                        member_partner = self.get_by_id(member.partner_id)
                        member_partner.sponsored_by_family = sponsor.family

                    sponsor.sponsor_for_family = member.family
                    if sponsor.partner_id is not None:
                        sponsor_partner = self.get_by_id(sponsor.partner_id)
                        sponsor_partner.sponsor_for_family = member.family

    @staticmethod
    def __is_within_sponsor_period(member):
        return member.start_date and (today - member.start_date).days < 90

    def __members_by_id(self):
        return {x.id: x for x in self}

    def get_by_id(self, id):
        for member in self:
            if member.id == id:
                return member
        return None

    def get_family_name_by_family_id(self, family_id):
        for member in self:
            if member.family == family_id:
                return member.family_name

class Day():
    def __init__(self, date, members=[]):
        random.shuffle(members)
        self.date = date
        self.members = [None] * 2
        for m in members:
            self.put(m)

    @property
    def is_full(self):
        return len(self.members) >= 2 and self.members[0] is not None and self.members[1] is not None

    @property
    def tallen(self):
        return self.members[0] if self.members else None

    @property
    def granen(self):
        return self.members[1] if self.members and len(self.members) == 2 else None

    def put(self, member, department=None):
        if self.is_full:
            raise TooManyMembersOnDayError

        if department == TALLEN_ID:
            if not self.tallen:
                self.members[0] = member
            else:
                raise DepartmentNotAvailableError
        elif department == GRANEN_ID and not self.granen:
            if not self.granen:
                self.members[1] = member
            else:
                raise DepartmentNotAvailableError
        else:
            if not self.tallen:
                self.members[0] = member
            elif not self.granen:
                self.members[1] = member

    def contains_family(self, family):
        for m in self.members:
            if m and m.family == family:
                return True
        return False

    def __repr__(self):
        return "<%s T: %s, G: %s>" % (self.date, self.tallen, self.granen)


class DayList(list):
    def __init__(self, work_days_service):
        self.work_days_service = work_days_service

    def append_member(self, member: Member, department=None):
        if len(self) == 0:
            last_day = Day(self.work_days_service.next())
            self.append(last_day)
        else:
            last_day = self[-1]

        if last_day.is_full:
            last_day = Day(self.work_days_service.next())
            self.append(last_day)

        if DayList.is_day_within_members_end_grace_period(member, last_day) \
                or DayList.is_day_within_members_start_grace_period(member, last_day):
            return

        last_day.put(member, department)

    @staticmethod
    def is_day_within_members_end_grace_period(member, day):
        if member.end_date:
            member_end_date = member.end_date
            prev_month_date = DayList.prev_month(member_end_date)
            day_date = datetime.strptime(day.date, "%Y-%m-%d").date()
            return prev_month_date < day_date
        return False

    @staticmethod
    def is_day_within_members_start_grace_period(member, day):
        if member.start_date:
            member_start_date = member.start_date
            next_month_date = DayList.next_month(member_start_date)
            day_date = datetime.strptime(day.date, "%Y-%m-%d").date()
            return day_date < next_month_date
        return False

    @staticmethod
    def prev_month(date):
        if date.month == 1:
            return date.replace(month=12, year=date.year - 1)
        else:
            try:
                return date.replace(month=date.month - 1)
            except ValueError:
                return DayList.prev_month(date=date.replace(day=date.day - 1))

    @staticmethod
    def next_month(date):
        if date.month == 12:
            return date.replace(month=1, year=date.year + 1)
        else:
            try:
                return date.replace(month=date.month + 1)
            except ValueError:
                return DayList.prev_month(date=date.replace(day=date.day - 1))

    @property
    def members(self):
        members = []
        for day in self:
            members.extend(day.members)
        return members
