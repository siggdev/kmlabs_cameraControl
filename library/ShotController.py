from .RedisDriver import RedisDriver


class ShotController:
    def __init__(self):
        self.redis = RedisDriver()

    def get_next_shot_time(self):
        next_shot = self.redis.lrange('shot_times', 0, 0)

        if len(next_shot) > 0:
            return next_shot[0]

        return None