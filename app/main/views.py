"""Metadata server help page views"""
from flask import render_template

from . import main


@main.route('/')
def index():
    """Help page"""

    return render_template('index.html')

@main.route('/hydrograph_vis')
def hydrograph_visualization():
    """
    This function is for hydrograph visualization
    """

    return render_template('hydrograph_vis.html')


