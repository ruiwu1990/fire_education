"""
PRMS Fire Modeling API

Date: Feb 25 2016
"""
from flask import jsonify, request, Response, render_template
import json

from netCDF4 import Dataset
from json import dumps
from pprint import pprint
import json
import netCDF4    
import numpy  
import os

from . import api


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


def add_values_into_json():

    # find path
    app_root = os.path.dirname(os.path.abspath(__file__))
    download_dir = app_root + '/../static/data/'
    file_full_path = download_dir + 'parameter.nc'

    fileHandle = Dataset(file_full_path, 'r')
    #temporaryFileHandle = open('vegetation_type.json', 'w')
        
    dimensions = [dimension for dimension in fileHandle.dimensions]

    for dimension in dimensions: 
        if dimension == 'lat':
            numberOfLatitudeValues = len(fileHandle.dimensions[dimension])
        if dimension == 'lon':
            numberOfLongitudeValues = len(fileHandle.dimensions[dimension])

    latitudeValues = fileHandle.variables['lat'][:]
    longitudeValues = fileHandle.variables['lon'][:]
    lower_left_latitude =latitudeValues[numberOfLatitudeValues-1]
    lower_left_longitude =longitudeValues[0]
    upper_right_latitude =latitudeValues[0]
    upper_right_longitude =longitudeValues[numberOfLongitudeValues-1]

    variables = [variable for variable in fileHandle.variables]
    variableValues = fileHandle.variables['cov_type'][:,:]
    listOfVariableValues = []

    for i in range(numberOfLatitudeValues):
        for j in range(len(variableValues[i])):
            listOfVariableValues.append(int(variableValues[i][j]))

    #print listOfVariableValues

    indexOfZeroValues = []
    indexOfOneValues = []
    indexOfTwoValues = []
    indexOfThreeValues = []
    indexOfFourValues = []

    for index in [index for index, value in enumerate(listOfVariableValues) if value == 0]:
        indexOfZeroValues.append(index)
    for index in [index for index, value in enumerate(listOfVariableValues) if value == 1]:
        indexOfOneValues.append(index)
    for index in [index for index, value in enumerate(listOfVariableValues) if value == 2]:
        indexOfTwoValues.append(index)
    for index in [index for index, value in enumerate(listOfVariableValues) if value == 3]:
        indexOfThreeValues.append(index)
    for index in [index for index, value in enumerate(listOfVariableValues) if value == 4]:
        indexOfFourValues.append(index)

    data = { 
              'vegetation_map': 
              { 
                '0': { 
                        'HRU_number': indexOfZeroValues 
                     }, 
                '1': { 
                        'HRU_number': indexOfOneValues 
                     }, 
                '2': { 
                        'HRU_number': indexOfTwoValues 
                     }, 
                '3': { 
                        'HRU_number': indexOfThreeValues 
                     }, 
                '4': { 
                        'HRU_number': indexOfFourValues 
                     } 
              }, 
              'projection_information': 
              { 
                'ncol': numberOfLongitudeValues, 
                'nrow': numberOfLatitudeValues, 
                'xllcorner': lower_left_latitude, 
                'yllcorner': lower_left_longitude, 
                'xurcorner': upper_right_latitude, 
                'yurcorner' : upper_right_longitude, 
                'cellsize(m)': 100 
              } 
            }
    
    return jsonify(data)

@api.route('/visualize')
def visualize_2d_map():
    """visualize data on map"""
    return render_template('vis/index.html')

@api.route('/api/base-veg-map', methods=['GET','POST'])
def hru_veg_json():
    if request.method == 'GET':
        """generate json file from netcdf file"""
        # TODO this part needs to be improved
        # enable to choose different nc file
        return add_values_into_json()
    else:
        """TODO modify netcdf based on json"""
        return