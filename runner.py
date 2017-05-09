from generator.integration.database import MembersDAO, ClosedDaysDAO
from generator.generator import Generator
from generator.integration.workdays import WorkDays
from generator.integration.dryg import DrygDAO


members = MembersDAO().get_members_for_sos_generator()

g = Generator(members=members, holy_period_length=25)
g.generate()

work_days = WorkDays(start_after_date="2017-05-31", closed_days_dao=ClosedDaysDAO(), dryg_dao=DrygDAO())
for i, day in enumerate(g.sos_days):
    print("%s: %s" % (work_days.next(), day))

print("Number of tries: %s" % g.number_of_retries_done)
