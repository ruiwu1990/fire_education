"""
visualize blueprint: visualize map and enable users to choose area to change veg code
"""
from flask import Blueprint

visualize = Blueprint('visualize', __name__)

from . import views
