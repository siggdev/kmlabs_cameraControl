from flask import render_template, request
from .SunTimesLoader import SunTimesLoader
from .ShotController import ShotController


class WebController:
    def __init__(self, flask_app):
        self.app = flask_app

    def serveIndexPage(self):
        # load sun info
        sun_times = SunTimesLoader()

        # calculate time until next shot
        shot_controller = ShotController()

        return render_template('index.html', sun_times=sun_times, shot_controller=shot_controller)

    def changeSettings(self):
        return request.data
