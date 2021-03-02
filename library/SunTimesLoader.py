import requests
from datetime import date


class SunTimesLoader:
    def __init__(self, lat=48.137154, lng=11.576124, request_date=date.today(), utc=False):
        self.lat = lat
        self.lng = lng
        self.utc = utc
        self.date = request_date

        response = self.__request_api()

    def __request_api(self):
        request_date = self.date.strftime("%Y-%m-%d")
        request_uri = ('https://api.sunrise-sunset.org/json?lat='
                       + str(self.lat)
                       + '&lng='
                       + str(self.lng)
                       + '&date='
                       + request_date
                       + '&formatted=0')
        return requests.get(request_uri)
