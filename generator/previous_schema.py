from datetime import datetime

class PreviousSchema:
    def __init__(self, previous_schedule_path):
        schedule_file = open(previous_schedule_path, "r")
        # Read header, to skip it
        schedule_file.readline()
        self.days = []
        for line in schedule_file:
            split_line = line.strip().split(";")
            self.days.append(ScheduledDay(datetime.strptime(split_line[0], '%Y-%m-%d').date(), split_line[1], split_line[2]))
        schedule_file.close()



class ScheduledDay:
    def __init__(self, date, tallen_cleaner, granen_cleaner):
        self.date = date
        self.tallen_cleaner = tallen_cleaner
        self.granen_cleaner = granen_cleaner