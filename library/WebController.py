from flask import render_template


class WebController:
    def __init__(self, flask_app):
        self.app = flask_app

    def serveIndexPage(self):
        return render_template('index.html')

    def changeSettings(self):
        return render_template('index.html')
