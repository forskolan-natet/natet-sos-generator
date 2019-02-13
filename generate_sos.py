from generator.integration.database import MembersDAO, ClosedDaysDAO, SchedulePlanningDAO, ScheduleLiveDAO
from generator.generator import Generator
from generator.integration.workdays import WorkDaysService
from generator.integration.dryg import DrygDAO
from generator.model import Day, DayList, MemberList
from generator.constants import TALLEN_ID, GRANEN_ID


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
        text = "%s\t%s\t%s" % (day.date, "Tallen" if member is day.tallen else "Granen", member.name)
        if member.family in sos_per_family:
            sos_per_family[member.family].append(text)
        else:
            sos_per_family[member.family] = [text]

for family_id, sos_list in sos_per_family.items():
    print("\n%s:" % members.get_family_name_by_family_id(family_id))
    for sos in sos_list:
        print(sos)

print("\n\nShall we store in database? (y/n)")
choice = input().lower()
if choice == 'y':
    print("Fuck yeah!")
    store_sos(g.sos_days)
else:
    print("Hell no!")
