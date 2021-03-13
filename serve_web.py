from library.WebController import WebController
from flask import Flask

app = Flask('CamControl', template_folder='templates', static_folder='assets')
controller = WebController(app);


@app.route('/', methods=['GET'])
def index():
    return controller.serveIndexPage()


@app.route('/', methods=['POST'])
def save():
    return controller.changeSettings()


app.run('localhost', 5000, True);
