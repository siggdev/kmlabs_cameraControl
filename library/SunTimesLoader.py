import json
import requests
from RedisDriver import RedisDriver
from datetime import date, datetime, timezone, timedelta


class SunTimesLoader:
    def __init__(self, lat=48.137154, lng=11.576124, request_date=date.today(), utc=False):
        self.red = RedisDriver()
        self.lat = lat
        self.lng = lng
        self.utc = utc
        self.date = request_date

        if self.__request_api():
            self.valid = True
            self.__parse_times()
        else:
            self.valid = False

    def __request_api(self):
        request_date = self.date.strftime("%Y-%m-%d")
        request_uri = ('https://api.sunrise-sunset.org/json?lat='
                       + str(self.lat)
                       + '&lng='
                       + str(self.lng)
                       + '&date='
                       + request_date
                       + '&formatted=0')

        response = requests.get(request_uri)

        if response.status_code != 200:
            return False

        self.__api_result = json.loads(response.text)

        if self.__api_result['status'] != 'OK':
            return False

        return True

    def __parse_times(self):
        self.sunrise = self.__parse_time('sunrise')
        self.sunset = self.__parse_time('sunset')
        self.solar_noon = self.__parse_time('solar_noon')
        self.day_length = timedelta(seconds=int(self.__api_result['day_length']))
        self.civil_twilight_begin = self.__parse_time('civil_twilight_begin')
        self.civil_twilight_end = self.__parse_time('civil_twilight_end')
        self.nautical_twilight_begin = self.__parse_time('nautical_twilight_begin')
        self.nautical_twilight_end = self.__parse_time('nautical_twilight_end')
        self.astronomical_twilight_begin = self.__parse_time('astronomical_twilight_begin')
        self.astronomical_twilight_end = self.__parse_time('astronomical_twilight_end')

    def __parse_time(self, value):
        parsed_time = datetime.fromisoformat(self.__api_result[value])
        if not self.utc:
            parsed_time = parsed_time.replace(tzinfo=timezone.utc).astimezone(tz=None)
        return parsed_time

    def set_location(self, lat, lng):
        try:
            self.lat = float(lat)
            self.lng = float(lng)
        except ValueError:
            return False

        return True

    def set_utc(self, utc):
        if utc:
            self.utc = True
        else:
            self.utc = False

    def set_request_date(self, request_date):
        if not isinstance(request_date, datetime):
            return False
        self.date = request_date
        return True

    def do_request(self):
        if self.__request_api():
            self.__parse_times()
            self.valid = True
            return self.valid
        self.valid = False
        return self.valid

    def write_to_redis(self):
        self.red.hset('suntimes', 'date', self.date)
        self.red.hset('suntimes', 'sunrise', self.sunrise)
        self.red.hset('suntimes', 'sunset', self.sunset)
        self.red.hset('suntimes', 'solar_noon', self.solar_noon)
        self.red.hset('suntimes', 'day_length', self.day_length)
        self.red.hset('suntimes', 'civil_twilight_begin', self.civil_twilight_begin)
        self.red.hset('suntimes', 'civil_twilight_end', self.civil_twilight_end)
        self.red.hset('suntimes', 'nautical_twilight_begin', self.nautical_twilight_begin)
        self.red.hset('suntimes', 'nautical_twilight_end', self.nautical_twilight_end)
        self.red.hset('suntimes', 'astronomical_twilight_begin', self.astronomical_twilight_begin)
        self.red.hset('suntimes', 'astronomical_twilight_end', self.astronomical_twilight_end)