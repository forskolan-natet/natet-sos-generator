import requests


class DrygDAO:
    def get_days_for_year(self, year):
        response = requests.get("http://api.dryg.net/dagar/v2.1/%s" % year)
        data = response.json()
        workdays = [x["datum"] for x in data["dagar"] if x["arbetsfri dag"] == "Nej"]
        return workdays
