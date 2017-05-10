import random
from datetime import datetime

from .exceptions import TooManyMembersOnDayError


class Member:
    def __init__(self, id=0, first_name="", last_name="", sos_percentage=100, family=0, sponsor_for_family=None,
                 sponsored_by_family=None, end_date=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.sos_percentage = sos_percentage
        self.family = family
        self.sponsor_for_family = sponsor_for_family
        self.sponsored_by_family = sponsored_by_family
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
        return members


class Day():
    def __init__(self, date, members=[]):
        random.shuffle(members)
        self.date = date
        self.members = []
        for m in members:
            self.put(m)

    @property
    def is_full(self):
        return len(self.members) >= 2

    @property
    def tallen(self):
        return self.members[0] if self.members else None

    @property
    def granen(self):
        return self.members[1] if self.members and len(self.members) == 2 else None

    def put(self, member):
        if self.is_full:
            raise TooManyMembersOnDayError
        self.members.append(member)
        random.shuffle(self.members)

    def contains_family(self, family):
        for m in self.members:
            if m.family == family:
                return True
        return False

    def __repr__(self):
        return "<%s T: %s, G: %s>" % (self.date, self.tallen, self.granen)


class DayList(list):
    def __init__(self, work_days_service):
        self.work_days_service = work_days_service

    def append_member(self, member: Member):
        if len(self) == 0:
            last_day = Day(self.work_days_service.next())
            self.append(last_day)
        else:
            last_day = self[-1]

        if last_day.is_full:
            last_day = Day(self.work_days_service.next())
            self.append(last_day)

        if DayList.is_day_withing_members_end_grace_period(member, last_day):
            return

        last_day.put(member)

    @staticmethod
    def is_day_withing_members_end_grace_period(member, day):
        if member.end_date:
            member_end_date = member.end_date
            prev_month_date = DayList.prev_month(member_end_date)
            day_date = datetime.strptime(day.date, "%Y-%m-%d").date()
            return prev_month_date < day_date
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

    @property
    def members(self):
        members = []
        for day in self:
            members.extend(day.members)
        return members
