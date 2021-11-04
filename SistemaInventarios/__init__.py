from flask import Flask
import dash

serverFlask = Flask(__name__)

appDash = dash.Dash(__name__, server=serverFlask, url_base_pathname='/dash/')
appDash.config['suppress_callback_exceptions'] = True

from SistemaInventarios import rutas
