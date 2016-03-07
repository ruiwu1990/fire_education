"""
VW Platform Application Package Constructor
"""
from flask import Flask
from flask_cors import CORS

# if there is an exception, we are running tests
try:
    from config import config
except ImportError:
    from ..config import config


# enable cross-origin resource sharing for the REST API
cors = CORS(resources={r'/api/*': {'origins': '*'}})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    cors.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
