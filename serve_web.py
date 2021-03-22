from library.WebController import WebController
from flask import Flask, redirect

app = Flask('CamControl', template_folder='templates', static_folder='assets')
controller = WebController(app);


@app.route('/', methods=['GET'])
def index():
    return controller.serveIndexPage()


@app.route('/', methods=['POST'])
def save():
    return controller.changeSettings()


@app.route('/getseconds', methods=['GET'])
def getSecs():
    return controller.returnSecondsToNextShot()


@app.route('/favicon.ico', methods=['GET'])
def serveFavicon():
    redirect('assets/favicon.ico')


app.run('localhost', 5000, True);
