from datetime import datetime

class PreviousSchema:
    @staticmethod
    def parse(previous_schedule_path):
        schedule_file = open(previous_schedule_path, "r")
        # Read header, to skip it
        schedule_file.readline()
        previous_schedule = []
        for line in schedule_file:
            split_line = line.strip().split(";")
            previous_schedule.append(ScheduledDay(datetime.strptime(split_line[0], '%Y-%m-%d').date(), split_line[1], split_line[2]))
        schedule_file.close()
        return previous_schedule


class ScheduledDay:
    def __init__(self, date, tallen_cleaner, granen_cleaner):
        self.date = date
        self.tallen_cleaner = tallen_cleaner
        self.granen_cleaner = granen_cleaner