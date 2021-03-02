import re
from redis import Redis
from datetime import datetime, timedelta, date


class RedisDriver:
    def __init__(self):
        self.redis = Redis(decode_responses=True)

        self.__iso_datetime_regex = (
            r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|['
            r'01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5]['
            r'0-9])?$')

        self.__iso_date_regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])?$'


    def __parse_datetime_if_iso_format(self, value):
        if re.fullmatch(self.__iso_datetime_regex, value) is not None:
            return datetime.fromisoformat(value)
        else:
            return False

    def __parse_date_if_iso_format(self, value):
        if re.fullmatch(self.__iso_date_regex, value) is not None:
            return date.fromisoformat(value)
        else:
            return False

    def hset(self, name, key, value):
        if isinstance(value, datetime):
            redis_value = value.isoformat()
        elif isinstance(value, date):
            redis_value = value.isoformat()
        elif isinstance(value, timedelta):
            redis_value = value.seconds
        else:
            redis_value = value

        self.redis.hset(name, key, redis_value)

    def hget(self, name, key):
        value = self.redis.hget(name, key)

        if not value:
            return None

        dt = self.__parse_datetime_if_iso_format(value)
        if dt:
            return dt

        d = self.__parse_date_if_iso_format(value)
        if d:
            return d

        return value
