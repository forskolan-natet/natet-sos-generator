from generator.integration.database import MembersDAO, ClosedDaysDAO, SchedulePlanningDAO, GroupDAO
from generator.generator import Generator
from generator.integration.workdays import WorkDaysService
from generator.integration.dryg import DrygDAO
from generator.integration.database import ScheduleLiveDAO
from generator.model import MemberList
from generator.constants import TALLEN_ID, GRANEN_ID


members_dicts = MembersDAO().get_members_for_sos_generator()
members = MemberList.create_from_dicts(members_dicts)

start_after_date = ScheduleLiveDAO().get_last_scheduled_date()
work_days_service = WorkDaysService(start_after_date=start_after_date,
                                    closed_days_dao=ClosedDaysDAO(),
                                    dryg_dao=DrygDAO())

g = Generator(members=members, work_days_service=work_days_service)
g.generate()

schedule_planning_dao = SchedulePlanningDAO()
for day in g.sos_days:
    schedule_planning_dao.add_sos(day.date, TALLEN_ID, day.tallen.id)
    schedule_planning_dao.add_sos(day.date, GRANEN_ID, day.granen.id)

print("Number of tries: %s" % g.number_of_retries_done)

sos_per_family = {}
for day in g.sos_days:
    print("%s Tallen: %s, Granen: %s" % (day.date, day.tallen.name, day.granen.name))
    for member in day.members:
        text = "%s %s %s" % (day.date, "Tallen" if member is day.tallen else "Granen", member.name)
        if member.family in sos_per_family:
            sos_per_family[member.family].append(text)
        else:
            sos_per_family[member.family] = [text]

groups = GroupDAO().get_groups()
for family_id, sos_list in sos_per_family.items():
    print("\nFamiljen %s:" % groups[family_id].name)
    for sos in sos_list:
        print(sos)

