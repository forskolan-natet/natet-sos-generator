class WorkDaysService:
    current_index = 0

    def __init__(self, start_after_date, closed_days_dao, dryg_dao):
        self.start_after_date = start_after_date
        start_year = start_after_date[:4]
        self.work_days = dryg_dao.get_days_for_year(start_year)
        index_of_start_after_date = self.work_days.index(start_after_date)
        self.work_days.extend(dryg_dao.get_days_for_year(int(start_year) + 1))
        self.work_days = self.work_days[index_of_start_after_date + 1:]
        closed_days = closed_days_dao.parse_closed_days()
        for closed_day in closed_days:
            if closed_day in self.work_days:
                self.work_days.remove(closed_day)

    def reset(self):
        self.current_index = 0

    def next(self):
        next_work_day = self.work_days[self.current_index]
        self.current_index += 1
        return next_work_day
