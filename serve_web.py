from library.WebController import WebController
from flask import Flask, redirect
from waitress import serve

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


@app.route('/makeshot', methods=['GET'])
def makeShot():
    return controller.makeManualShot()
    

#app.run('localhost', 5000, True)
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)
