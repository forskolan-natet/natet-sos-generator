import requests


class DrygDAO:
    def __init__(self):
        pass

    def get_days_for_year(self, year):
        response = requests.get("https://sholiday.faboul.se/dagar/v2.1/%s" % year)
        data = response.json()
        workdays = [x["datum"] for x in data["dagar"] if x["arbetsfri dag"] == "Nej"]
        return workdays
