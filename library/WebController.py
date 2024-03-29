from flask import render_template, request, Response
from .SunTimesLoader import SunTimesLoader
from .ShotTimeCalculator import ShotTimeCalculator
from .ShotController import ShotController
from .RedisDriver import RedisDriver


class WebController:
    def __init__(self, flask_app):
        self.app = flask_app
        self.shot_controller = ShotController()
        self.redis = RedisDriver()
        self.days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def serveIndexPage(self):
        # load sun info
        sun_times = SunTimesLoader()
        shot_settings = self.__get_actual_shot_settings()

        return render_template('index.html', sun_times=sun_times, shot_settings=shot_settings, shot_controller=self.shot_controller)

    def returnSecondsToNextShot(self):
        remaining_time = self.shot_controller.calculate_time_until_next_shot()
        
        if remaining_time is None:
            return "{ 'seconds': -1 }"
        
        return '{ "seconds": ' + str(remaining_time.seconds) + " }"

    def makeManualShot(self):
        self.shot_controller.make_shot()
        return 'OK'

    def changeSettings(self):
        # load sun info
        sun_times = SunTimesLoader()

        # validate input
        errors = self.__validate_inputs()
        if errors['bad_request']:
            return Response('invalid', 400)

        if errors['exist']:
            return render_template('index.html', sun_times=sun_times, shot_settings=request.form, shot_controller=self.shot_controller, errors=errors)

        for day in self.days:
            if day in request.form:
                self.redis.hset('shot_time_settings', day, 1)
            else:
                self.redis.hset('shot_time_settings', day, 0)

        self.redis.hset('shot_time_settings', 'start_time', request.form['start_time'])
        self.redis.hset('shot_time_settings', 'stop_time', request.form['stop_time'])
        self.redis.hset('shot_time_settings', 'interval', int(request.form['interval']))

        if(request.form['start_time'] == 'individual'):
            self.redis.hset('shot_time_settings', 'start_individual_hour', request.form['start_time_hvalue'])
            self.redis.hset('shot_time_settings', 'start_individual_minute', request.form['start_time_mvalue'])

        if(request.form['stop_time'] == 'individual'):
            self.redis.hset('shot_time_settings', 'stop_individual_hour', request.form['stop_time_hvalue'])
            self.redis.hset('shot_time_settings', 'stop_individual_minute', request.form['stop_time_mvalue'])

        if request.form['changeat'] == 'adhoc':
            shot_calc = ShotTimeCalculator()
            sun_times.write_to_redis()
            shot_calc.calculate_shot_times()
            shot_calc.write_to_redis()

        return render_template('index.html', sun_times=sun_times, shot_settings=request.form, shot_controller=self.shot_controller, errors=errors)

    def __validate_inputs(self):

        # initialize error array
        errors = {}
        errors['bad_request'] = False

        # define valid values
        valid_start_settings = ['sunrise', 'civil', 'nautical', 'astronomical', 'individual']
        valid_stop_settings = ['sunset', 'civil', 'nautical', 'astronomical', 'individual']
        valid_change_time_settings = ['adhoc', 'tomorrow']

        # validate start setting
        if request.form['start_time'] not in valid_start_settings:
            errors['bad_request'] = True
            return errors
        
        # validate stop setting
        if request.form['stop_time'] not in valid_stop_settings:
            errors['bad_request'] = True
            return errors

        # validate changeat values
        if request.form['changeat'] not in valid_change_time_settings:
            errors['bad_request'] = True
            return errors

        # validate individual start time values
        errors['indiv_start_time'] = []
        if request.form['start_time'] == 'individual':
            try:
                start_hour = int(request.form['start_time_hvalue'])
                if not (0 <= start_hour < 24):
                    errors['indiv_start_time'].append('Die Startzeit muss eine g&uuml;tige Zeit sein')
            except:
                errors['indiv_start_time'].append('Die Stundenangabe der Startzeit muss eine Zahl sein')

            try:
                start_minute = int(request.form['start_time_mvalue'])
                if not (0 <= start_minute < 60):
                    errors['indiv_start_time'].append('Die Startzeit muss eine g&uuml;tige Zeit sein')
            except:
                errors['indiv_start_time'].append('Die Minutenangabe der Startzeit muss eine Zahl sein')

        # validate individual stop time values
        errors['indiv_stop_time'] = []
        if request.form['stop_time'] == 'individual':
            try:
                stop_hour = int(request.form['stop_time_hvalue'])
                if not (0 <= stop_hour < 24):
                    errors['indiv_stop_time'].append('Die Stopzeit muss eine g&uuml;tige Zeit sein')
            except:
                errors['indiv_stop_time'].append('Die Stundenangabe der Stopzeit muss eine Zahl sein')

            try:
                stop_minute = int(request.form['stop_time_mvalue'])
                if not (0 <= stop_minute < 60):
                    errors['indiv_stop_time'].append('Die Stopzeit muss eine g&uuml;tige Zeit sein')
            except:
                errors['indiv_stop_time'].append('Die Stundenangabe der Stopzeit muss eine Zahl sein')

        # validate interval
        errors['interval'] = []
        try:
            interval = int(request.form['interval'])
            if not (0 < interval < 1200):
                errors['interval'].append('Das Intervall muss eine Minutenangabe zwischen 1 und 1200 sein')
        except:
            errors['interval'].append('Das Intervall muss eine Zahl sein')

        errors['exist'] = errors['interval'] or errors['indiv_stop_time'] or errors['indiv_start_time']

        return errors

    def __get_actual_shot_settings(self):

        shot_settings = {}

        #get shot days
        for day in self.days:
            if self.redis.hget('shot_time_settings', day) == '1':
                shot_settings[day] = 'on'
        
        #get start time
        shot_settings['start_time'] = self.redis.hget('shot_time_settings', 'start_time')
        if shot_settings['start_time'] is None:
            shot_settings['start_time'] = 'sunrise'

        if shot_settings['start_time'] == 'individual':
            shot_settings['start_time_hvalue'] = self.redis.hget('shot_time_settings', 'start_individual_hour')
            if shot_settings['start_time_hvalue'] is None:
                shot_settings['start_time_hvalue'] = 6
            else:
                shot_settings['start_time_hvalue'] = int(shot_settings['start_time_hvalue'])

            
            shot_settings['start_time_mvalue'] = self.redis.hget('shot_time_settings', 'start_individual_minute')
            if shot_settings['start_time_mvalue'] is None:
                shot_settings['start_time_mvalue'] = 6
            else:
                shot_settings['start_time_mvalue'] = int(shot_settings['start_time_mvalue'])

        #get stop time
        shot_settings['stop_time'] = self.redis.hget('shot_time_settings', 'stop_time')
        if shot_settings['stop_time'] is None:
            shot_settings['stop_time'] = 'sunset'


        if shot_settings['stop_time'] == 'individual':
            shot_settings['stop_time_hvalue'] = self.redis.hget('shot_time_settings', 'stop_individual_hour')
            if shot_settings['stop_time_hvalue'] is None:
                shot_settings['stop_time_hvalue'] = 6
            else:
                shot_settings['stop_time_hvalue'] = int(shot_settings['stop_time_hvalue'])

            
            shot_settings['stop_time_mvalue'] = self.redis.hget('shot_time_settings', 'stop_individual_minute')
            if shot_settings['stop_time_mvalue'] is None:
                shot_settings['stop_time_mvalue'] = 6
            else:
                shot_settings['stop_time_mvalue'] = int(shot_settings['stop_time_mvalue'])

        #get interval
        shot_settings['interval'] = self.redis.hget('shot_time_settings', 'interval')
        if shot_settings['interval'] is None:
            shot_settings['interval'] = 10
        else:
            shot_settings['interval'] = int(shot_settings['interval'])

        return shot_settings
