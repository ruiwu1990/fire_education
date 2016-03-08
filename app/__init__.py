"""
VW Platform Application Package Constructor
"""
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from config import config


db = MongoEngine()

# enable cross-origin resource sharing for the REST API
cors = CORS(resources={r'/api/*': {'origins': '*'}})


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    cors.init_app(app)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
