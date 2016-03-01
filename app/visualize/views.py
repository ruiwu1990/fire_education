"""Metadata server help page views"""
from flask import render_template

from . import visualize


@visualize.route('/visualize')
def visualize_2d_map():
    """visualize data on map"""

    return render_template('vis/index.html')

# @visualize.route('/visualize/veg_json')
# def send_veg_json():
#     """visualize data on map"""

#     return render_template('vis/index.html')