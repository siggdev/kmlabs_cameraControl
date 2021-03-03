from .RedisDriver import RedisDriver
from datetime import datetime


class ShotController:
    def __init__(self):
        self.redis = RedisDriver()

    def get_next_shot_time(self):
        next_shot = self.redis.lrange('shot_times', 0, 0)

        if len(next_shot) > 0:
            return next_shot[0]

        return None

    def check_if_next_shot_is_due(self):
        actual_time = datetime.now().replace(tzinfo=None).astimezone(tz=None)
        next_shot = self.get_next_shot_time()

        if next_shot and next_shot < actual_time:
            return True

        return False

