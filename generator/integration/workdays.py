import requests


def get_for_year(year):
    response = requests.get("http://api.dryg.net/dagar/v2.1/%s" % year)
    data = response.json()
    workdays = [x["datum"] for x in data["dagar"] if x["arbetsfri dag"] == "Nej"]
    return workdays


def get_x_number_of_days_from_date(x, start_after_date):
    start_year = start_after_date[:4]
    work_days = get_for_year(start_year)

    index_of_start_after_date = work_days.index(start_after_date)
    work_days = work_days[index_of_start_after_date + 1:]

    while x > len(work_days):
        next_year = int(start_year) + 1
        work_days.extend(get_for_year(next_year))

    return work_days
