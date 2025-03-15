from datetime import datetime, timedelta

class ClosedDays:
    def __init__(self, closed_days_path):
        self.closed_days_path = closed_days_path

    def parse_closed_days(self):
        closed_file = open(self.closed_days_path, "r")
        closed_days = []
        for line in closed_file:
            split_line = line.strip().split("<->")
            if len(split_line) == 1:
                closed_days.append(split_line[0])
            else:
                start_day = datetime.strptime(split_line[0], '%Y-%m-%d').date()
                last_day = datetime.strptime(split_line[1], '%Y-%m-%d').date()
                delta = last_day - start_day
                for i in range(delta.days + 1):
                    closed_days.append((start_day + timedelta(days = i)).strftime('%Y-%m-%d'))
        closed_file.close()
        return closed_days