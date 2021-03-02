import re
from redis import Redis
from datetime import datetime, timedelta


class RedisDriver:
    def __init__(self):
        self.redis = Redis(decode_responses=True)

        self.__iso_regex = re.compile(
            r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|['
            r'01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5]['
            r'0-9])?$')

    def __parse_datetime_if_iso_format(self, value):
        if self.__iso_regex.fullmatch(value) is not None:
            return datetime.fromisoformat(value)
        else:
            return False

    def hset(self, name, key, value):
        if isinstance(value, datetime):
            redis_value = value.isoformat()
        elif isinstance(value, timedelta):
            redis_value = value.seconds
        else:
            redis_value = value

        self.redis.hset(name, key, redis_value)

    def hget(self, name, key):
        value = self.redis.hget(name, key)

        date = self.__parse_datetime_if_iso_format(value)
        if date:
            return date

        return value
