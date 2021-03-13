from flask import render_template
from .SunTimesLoader import SunTimesLoader


class WebController:
    def __init__(self, flask_app):
        self.app = flask_app

    def serveIndexPage(self):
        sun_times = SunTimesLoader()
        return render_template('index.html', sun_times=sun_times)

    def changeSettings(self):
        return render_template('index.html')
