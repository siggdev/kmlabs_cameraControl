from library.SunTimesLoader import SunTimesLoader
from library.ShotTimeCalculator import ShotTimeCalculator

sun_times = SunTimesLoader()
sun_times.write_to_redis()

shot_time_calc = ShotTimeCalculator()
shot_time_calc.calculate_shot_times()
shot_time_calc.write_to_redis()
