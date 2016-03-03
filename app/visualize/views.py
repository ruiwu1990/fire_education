"""Metadata server help page views"""
from flask import render_template, request

import util

from . import visualize


@visualize.route('/visualize')
def visualize_2d_map():
    """visualize data on map"""

    return render_template('vis/index.html')



@visualize.route('/visualize/veg_json', methods=['GET','POST'])
def hru_veg_json():
    if request.method == 'GET':
        """generate json file from netcdf file"""
        # TODO this part needs to be improved
        # enable to choose different nc file
        return util.add_values_into_json()
    else:
        """TODO modify netcdf based on json"""
        return