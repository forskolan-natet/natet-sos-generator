class WorkDays:
    def __init__(self, start_after_date, closed_days_dao, dryg_dao):
        start_year = start_after_date[:4]
        self.last_fetched_year = int(start_year)
        self.work_days = dryg_dao.get_days_for_year(start_year)
        self.current_index = self.work_days.index(start_after_date)
        self.closed_days = closed_days_dao.get_closed_days()
        self.dryg_dao = dryg_dao

    def next(self):
        next_index = self.current_index + 1
        while next_index >= len(self.work_days):
            next_year = self.last_fetched_year + 1
            self.work_days.extend(self.dryg_dao.get_days_for_year(next_year))
            self.last_fetched_year = next_year

        next_work_day = self.work_days[next_index]
        self.current_index = next_index

        if next_work_day in self.closed_days:
            return self.next()

        return next_work_day
