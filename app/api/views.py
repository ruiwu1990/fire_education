"""
PRMS Fire Modeling API

Date: Feb 25 2016
"""
from flask import jsonify, request, Response
from flask_cors import cross_origin
import json

import netCDF4
import os

from . import api
from util import add_values_into_json


@api.route('/api/scenarios/<scenario_id>', methods=['GET', 'DELETE'])
def scenario_by_id(scenario_id):
    """
    Look up or delete a scenario by its id
    """
    if request.method == 'GET':
        try:
            return jsonify(EXAMPLE_SCENARIOS[int(scenario_id)])
        except:
            return Response(
                json.dumps(
                    {'message': 'no scenario id found! ' +
                                'currently the scenario id must be 1 or 0!'}
                ), 400, mimetype='application/json'
            )

    if request.method == 'DELETE':
        if scenario_id not in ['0', '1']:
            return Response(
                json.dumps(
                    {'message': 'no scenario id found! ' +
                                'currently the scenario id must be 1 or 0!'}
                ), 400, mimetype='application/json'
            )
        else:
            return jsonify(
                {
                    'message': 'scenario with id ' + scenario_id +
                               ' removed! (not really...)'
                }
            )


@api.route('/api/scenarios', methods=['GET', 'POST'])
def scenarios():
    """
    Handle get and push requests for list of all finished scenarios and submit
    a new scenario, respectively.
    """
    if request.method == 'GET':
        return jsonify(scenarios=EXAMPLE_SCENARIOS)
    else:
        return jsonify(
            {
                'message':
                'POST received! Soon you\'ll actually kick off a model!'
            }
        )


@api.route('/api/base-veg-map', methods=['GET'])
def hru_veg_json():
    if request.method == 'GET':
        """generate json file from netcdf file"""
        return jsonify(add_values_into_json())


ex_uu1 = '0'
ex_uu2 = '1'

EXAMPLE_SCENARIOS = [{
    'name': 'Smaller fire',
    'id': ex_uu1,
    'time_received': '2016-02-25T18:22:01',
    'time_finished': '2016-02-25T18:28:01',
    'input': {
        'control':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu1 + '/control.dat',
        'parameter':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu1 + '/params.nc',
        'data':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu1 + '/data.nc',
    },
    'output': {
        'animation':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu1 + '/control.dat',
        'data':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu1 + '/data.nc',
    },
    'fire_geometry': {
        'type': 'MultiPolygon',
        'coordinates': [
          [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0],
              [102.0, 3.0], [102.0, 2.0]]],
          [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
              [100.0, 1.0], [100.0, 0.0]],
           [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8],
              [100.2, 0.8], [100.2, 0.2]]]
          ]
    },
    'total_fire_area(km^2)': 40.5,
    'hydrograph': {
        '2015-10-31': 23.2,
        '2015-11-30': 18.5,
        '2015-12-31': 70.4
    }
},
    {
    'name': 'Larger fire',
    'id': ex_uu2,
    'time_received': '2016-02-25T18:22:01',
    'time_finished': '2016-02-25T18:28:01',
    'input': {
        'control':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu2 + '/control.dat',
        'parameter':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu2 + '/params.nc',
        'data':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu2 + '/data.nc',
    },
    'output': {
        'animation':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu2 + '/control.dat',
        'data':
            'https://prmstool.virtualwatershed.org/downloads/' +
            ex_uu2 + '/data.nc',
    },
    'fire_geometry': {
        'type': 'MultiPolygon',
        'coordinates': [
          [[[102.0, 1.0], [103.0, 2.0], [103.0, 3.0],
              [102.0, 3.0], [102.0, 2.0]]],
          [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
              [100.0, 1.0], [100.0, 0.0]],
           [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8],
              [100.2, 0.8], [100.2, 0.2]]]
          ]
    },
    'total_fire_area(km^2)': 60.0,
    'hydrograph': {
        '2015-10-31': 22.2,
        '2015-11-30': 8.15,
        '2015-12-31': 80.4
    }
}]
