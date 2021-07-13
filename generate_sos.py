# encoding: utf-8

from generator.integration.database import MembersDAO, ClosedDaysDAO, SchedulePlanningDAO, ScheduleLiveDAO
from generator.generator import Generator
from generator.integration.workdays import WorkDaysService
from generator.integration.dryg import DrygDAO
from generator.model import Day, DayList, MemberList
from generator.constants import TALLEN_ID, GRANEN_ID
from icalendar import Calendar, Event
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--extraTo', dest='extra_to', type=int, nargs='*', help='member id of the member who shall have one extra sos')
parser.add_argument('--lessTo', dest='less_to', type=int, nargs='*', help='member id of the member who shall have one less sos')
args = parser.parse_args()

extra_to = []
less_to = []
if args.extra_to:
    print("Extra SOS to %s\n" % args.extra_to)
    extra_to = args.extra_to
if args.less_to:
    print("Less SOS to %s\n" % args.less_to)
    less_to = args.less_to


def store_sos(sos_days):
    schedule_planning_dao = SchedulePlanningDAO()
    for day in sos_days:
        schedule_planning_dao.add_sos(day.date, TALLEN_ID, day.tallen.id)
        schedule_planning_dao.add_sos(day.date, GRANEN_ID, day.granen.id)


members_dicts = MembersDAO().get_members_for_sos_generator()
members = MemberList.create_from_dicts(members_dicts)

schedule_live_dao = ScheduleLiveDAO()
start_after_date = schedule_live_dao.get_last_scheduled_date()
print("Start at date %s\n" % start_after_date)
work_days_service = WorkDaysService(start_after_date=start_after_date,
                                    closed_days_dao=ClosedDaysDAO(),
                                    dryg_dao=DrygDAO())

for member in members:
    if member.id in extra_to:
        print("Extra SOS to %s with SOS percentage %s" % (member.name, member.sos_percentage))
        member.sos_percentage += 50
        print("Extra SOS to %s with SOS percentage %s\n" % (member.name, member.sos_percentage))
    if member.id in less_to and member.sos_percentage >= 50:
        print("Less SOS to %s with SOS percentage %s" % (member.name, member.sos_percentage))
        member.sos_percentage -= 50
        print("Less SOS to %s with SOS percentage %s\n" % (member.name, member.sos_percentage))

last_ten_days_dict = schedule_live_dao.get_last_ten_sos_days()
last_ten_days = DayList(work_days_service=None)
for date, day_members in last_ten_days_dict.items():
    day = Day(date, [members.get_by_id(day_members[0]), members.get_by_id(day_members[1])])
    last_ten_days.append(day)

g = Generator(members=members, work_days_service=work_days_service, last_ten_days=last_ten_days)
g.generate()

sos_per_family = {}
print("\n\nStäng och städ per datum")
for day in g.sos_days:
    print("%s\tTallen: %s,\tGranen: %s" % (day.date, day.tallen.name, day.granen.name))
    for member in day.members:
        obj = {
            'date': day.date,
            'department': "Tallen" if member is day.tallen else "Granen",
            'member': member.name
        }
        if member.family in sos_per_family:
            sos_per_family[member.family].append(obj)
        else:
            sos_per_family[member.family] = [obj]

for family_id, sos_list in sos_per_family.items():
    family_name = members.get_family_name_by_family_id(family_id)
    print("\n%s:" % family_name)
    cal = Calendar()
    for sos in sos_list:
        print("%s\t%s\t%s" % (sos['date'], sos['department'], sos['member']))
        event = Event()

        event.add('summary', 'Stäng och städ på %s' % sos['department'])
        date_parts = sos['date'].split('-')
        event.add('dtstart', datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]), 15, 0, 0))
        event.add('dtend', datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]), 18, 0, 0))
        cal.add_component(event)
    f = open('%s.ics' % family_name, 'wb')
    f.write(cal.to_ical())
    f.close()

print("\n\nShall we store in database? (y/n)")
choice = input().lower()
if choice == 'y':
    print("Fuck yeah!")
    store_sos(g.sos_days)
else:
    print("Hell no!")
