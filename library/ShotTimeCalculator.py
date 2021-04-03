from .RedisDriver import RedisDriver
from datetime import datetime, timedelta


class ShotTimeCalculator:
    def __init__(self):
        self.shot_times = []
        self.redis = RedisDriver()
        
    def calculate_shot_times(self):
        self.__get_settings_or_default()
        self.__make_nice_start_time()

        actual_time = datetime.now(tz=self.start_time.tzinfo)

        self.shot_times = []

        if self.start_time > actual_time:
            self.shot_times.append(self.start_time)

        time_counter = self.start_time

        while time_counter < self.stop_time:
            time_counter += self.interval
            if time_counter > actual_time:
                self.shot_times.append(time_counter)

    def __get_settings_or_default(self):
        start_time_setting = self.redis.hget('shot_time_settings', 'start_time')
        if start_time_setting:
            if start_time_setting == 'sunrise':
                self.start_time = self.redis.hget('suntimes', 'sunrise')
            elif start_time_setting == 'civil':
                self.start_time = self.redis.hget('suntimes', 'civil_twilight_begin')
            elif start_time_setting == 'nautical':
                self.start_time = self.redis.hget('suntimes', 'nautical_twilight_begin')
            elif start_time_setting == 'astronomical':
                self.start_time = self.redis.hget('suntimes', 'astronomical_twilight_begin')
            elif start_time_setting == 'individual':
                hour = int(self.redis.hget('shot_time_settings', 'start_individual_hour'))
                minute = int(self.redis.hget('shot_time_settings', 'start_individual_minute'))
                self.start_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            else:
                self.start_time = None
        else:
            self.start_time = self.redis.hget('suntimes', 'sunrise')

        if not self.start_time:
            self.start_time = datetime.now()
            self.start_time.replace(hour=6, minute=0, second=0, microsecond=0)


        stop_time_setting = self.redis.hget('shot_time_settings', 'stop_time')

        if stop_time_setting:
            if stop_time_setting == 'sunrise':
                self.stop_time = self.redis.hget('suntimes', 'sunset')
            elif stop_time_setting == 'civil':
                self.stop_time = self.redis.hget('suntimes', 'civil_twilight_end')
            elif stop_time_setting == 'nautical':
                self.stop_time = self.redis.hget('suntimes', 'nautical_twilight_end')
            elif stop_time_setting == 'astronomical':
                self.stop_time = self.redis.hget('suntimes', 'astronomical_twilight_end')
            elif stop_time_setting == 'individual':
                hour = int(self.redis.hget('shot_time_settings', 'stop_individual_hour'))
                minute = int(self.redis.hget('shot_time_settings', 'stop_individual_minute'))
                self.stop_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            else:
                self.stop_time = None
        else:
            self.stop_time = self.redis.hget('suntimes', 'sunset')

        if not self.stop_time:
            self.stop_time = datetime.now()
            self.stop_time.replace(hour=21, minute=0, second=0, microsecond=0)

        try:
            self.interval = timedelta(minutes=int(self.redis.hget('shot_time_settings', 'interval')))
        except TypeError:
            self.interval = timedelta(minutes=15)

    def __make_nice_start_time(self):
        # floor start time to minutes
        self.start_time = self.start_time - timedelta(seconds=self.start_time.second)

        # floor to 30 minutes, if interval is mod 30
        if (self.interval.seconds / 60) % 30 == 0:
            self.start_time = self.start_time - timedelta(minutes=self.start_time.minute % 30)
        # floor to 15 minutes, if interval is mod 15
        elif (self.interval.seconds / 60) % 15 == 0:
            self.start_time = self.start_time - timedelta(minutes=self.start_time.minute % 15)
        # floor to 10 minutes, if interval is mod 5
        elif (self.interval.seconds / 60) % 5 == 0:
            self.start_time = self.start_time - timedelta(minutes=self.start_time.minute % 10)

    def write_to_redis(self):
        self.redis.delete('shot_times')

        for shot_time in self.shot_times:
            self.redis.rpush('shot_times', shot_time)
