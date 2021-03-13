from .RedisDriver import RedisDriver
from datetime import datetime, timedelta
from time import sleep
#import RPi.GPIO as GPIO


class ShotController:
    def __init__(self):
        self.redis = RedisDriver()
#        GPIO.setmode(GPIO.BOARD)
#        GPIO.setwarnings(False)
#        GPIO.setup(3, GPIO.OUT, initial=GPIO.HIGH)

    def get_next_shot_time(self):
        next_shot = self.redis.lrange('shot_times', 0, 0)

        if len(next_shot) > 0:
            return next_shot[0]

        return None

    def calculate_time_until_next_shot(self):
        next_shot = self.get_next_shot_time()
        current_time = datetime.now().replace(tzinfo=None).astimezone(tz=None)

        return timedelta(seconds=672)

    def check_if_next_shot_is_due(self):
        actual_time = datetime.now().replace(tzinfo=None).astimezone(tz=None)
        next_shot = self.get_next_shot_time()

        if next_shot and next_shot < actual_time:
            return True

        return False

    def make_shot(self):
#        GPIO.output(3, GPIO.LOW)
        sleep(0.2)
#        GPIO.output(3, GPIO.HIGH)

    def make_shot_if_due(self):
        if self.check_if_next_shot_is_due():
            self.make_shot()

