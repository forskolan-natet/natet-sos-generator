from generator.integration import database
from generator.generator import Generator
from generator.integration import workdays


members = database.get_members_for_sos_generator()

g = Generator(members=members, holy_period_length=25)
g.generate()

work_days = workdays.get_x_number_of_days_from_date(len(g.sos_days), "2017-05-31")
z = []
for i, day in enumerate(g.sos_days):
    if day.granen.family == 15 or day.tallen.family == 15:
       z.append(i)
    print("%s: %s" % (work_days[i], day))

print("Number of tries: %s" % g.number_of_retries_done)

print(z[3] - z[2])
print(z[2] - z[1])
print(z[1] - z[0])
