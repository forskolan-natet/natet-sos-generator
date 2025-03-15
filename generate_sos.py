# encoding: utf-8

from generator.generator import Generator
from generator.integration.workdays import WorkDaysService
from generator.integration.dryg import DrygDAO
from generator.model import Day, DayList, MemberList

from generator.properties import Properties
from generator.previous_schema import PreviousSchema
from generator.closed_days import ClosedDays
from generator.members import MembersExcel

# Parse properties file
properties = Properties("properties.conf")

# Read previous schema
previous_schedule = PreviousSchema.parse(properties.previous_schema)
last_scheduled_date = previous_schedule[-1].date.strftime('%Y-%m-%d')

members_dicts = MembersExcel.read_member_dict(properties.members_path)
members = MemberList.create_from_dicts(members_dicts)

print("Start at date %s\n" % last_scheduled_date)
work_days_service = WorkDaysService(start_after_date=last_scheduled_date,
                                    closed_days_dao=ClosedDays(properties.closed_days_path),
                                    dryg_dao=DrygDAO())


for member_id in properties.extra_sos_to:
    member = members.get_by_id(member_id)
    member.sos_percentage += 50
    print("Extra SOS to %s. New SOS percentage is %s\n" % (member.name, member.sos_percentage))

for member_id in properties.less_sos_to:
    member = members.get_by_id(member_id)
    member.sos_percentage -= 50
    print("Less SOS to %s. New SOS percentage is %s\n" % (member.name, member.sos_percentage))

last_ten_days = DayList(work_days_service=None)
for scheduled_day in previous_schedule[-10:]:
    date = scheduled_day.date.strftime('%Y-%m-%d')
    day = Day(date, [members.get_by_id(scheduled_day.tallen_cleaner), members.get_by_id(scheduled_day.granen_cleaner)])
    last_ten_days.append(day)

g = Generator(members=members,
              work_days_service=work_days_service,
              min_nr_of_days_between_sos=properties.min_nr_of_days_between_sos,
              last_ten_days=last_ten_days)
g.generate()

sos_per_family = {}
sos_per_date_file = open("schedules/SoS per date.csv", "w")
print("\n\nStäng och städ per datum")
print("Datum;Tallen;Granen")
sos_per_date_file.write("Datum;Tallen;Granen\n")
for day in g.sos_days:
    print("%s;%s;%s" % (day.date, day.tallen.name, day.granen.name))
    sos_per_date_file.write("%s;%s;%s\n" % (day.date, day.tallen.name, day.granen.name))
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
sos_per_date_file.close()

family_schedule_name = "Family schedule " + g.sos_days[0].date + " - " + g.sos_days[-1].date + ".txt"
sos_per_family_file = open(family_schedule_name, "w")
for family_id, sos_list in sos_per_family.items():
    family_name = members.get_family_name_by_family_id(family_id)
    print("\n%s" % family_name)
    sos_per_family_file.write(family_name + "\n")
    for sos in sos_list:
        print("%s\t%s\t%s" % (sos['date'], sos['department'], sos['member']))
        sos_per_family_file.write("%s\t%s\t%s\n" % (sos['date'], sos['department'], sos['member']))
    sos_per_family_file.write("\n")
sos_per_family_file.close()

def store_sos_schedule(sos_days):
    schedule_name = "Schedule " + sos_days[0].date + " - " + sos_days[-1].date + ".csv"
    schedule_file = open(schedule_name, "w")
    schedule_file.write("Datum;Tallen;Granen\n")
    for sos_day in sos_days:
        schedule_file.write(sos_day.date + ";" + str(sos_day.tallen.id) + ";" + str(sos_day.granen.id) + "\n")
    schedule_file.close()

store_sos_schedule(g.sos_days)