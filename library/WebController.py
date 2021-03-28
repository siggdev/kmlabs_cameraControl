from flask import render_template, request
from .SunTimesLoader import SunTimesLoader
from .ShotController import ShotController


class WebController:
    def __init__(self, flask_app):
        self.app = flask_app
        self.shot_controller = ShotController()

    def serveIndexPage(self):
        # load sun info
        sun_times = SunTimesLoader()

        return render_template('index.html', sun_times=sun_times, shot_controller=self.shot_controller)

    def returnSecondsToNextShot(self):
        remaining_time = self.shot_controller.calculate_time_until_next_shot()
        
        if remaining_time is None:
            return "{ 'seconds': -1 }"
        
        return '{ "seconds": ' + str(remaining_time.seconds) + " }"

    def changeSettings(self):
        return str(request.form)
