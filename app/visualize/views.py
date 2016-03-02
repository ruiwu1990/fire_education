"""Metadata server help page views"""
from flask import render_template, request, jsonify

# lisa part lib
from netCDF4 import Dataset
from json import dumps
from pprint import pprint
import json
import netCDF4    
import numpy  
import os
#lisa part lib ends

from . import visualize


@visualize.route('/visualize')
def visualize_2d_map():
    """visualize data on map"""

    return render_template('vis/index.html')

# lisa part
# this should go into util file
def add_values_into_json():

    # Rui
    # find path
    app_root = os.path.dirname(os.path.abspath(__file__))
    download_dir = app_root + '/tempData/'
    file_full_path = download_dir + 'parameter.nc'
    # Rui ends

    # Rui changed here
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

    data = { \
              'vegetation_map': \
              { \
                '0': { \
                        'HRU_number': indexOfZeroValues \
                     }, \
                '1': { \
                        'HRU_number': indexOfOneValues \
                     }, \
                '2': { \
                        'HRU_number': indexOfTwoValues \
                     }, \
                '3': { \
                        'HRU_number': indexOfThreeValues \
                     }, \
                '4': { \
                        'HRU_number': indexOfFourValues \
                     } \
              }, \
              'projection_information': \
              { \
                'ncol': numberOfLongitudeValues, \
                'nrow': numberOfLatitudeValues, \
                'xllcorner': lower_left_latitude, \
                'yllcorner': lower_left_longitude, \
                'xurcorner': upper_right_latitude, \
                'yurcorner' : upper_right_longitude, \
                'cellsize(m)': 100 \
              } \
            }
            #   
    #temporaryFileHandle.write(dumps(data, temporaryFileHandle, sort_keys = True, indent=1))
    return jsonify(data)


@visualize.route('/visualize/veg_json', methods=['GET','POST'])
def hru_veg_json():
    if request.method == 'GET':
        """Lisa please add your uploading json file part here"""
        # TODO this part needs to be improved
        # enable to choose different nc file
        return add_values_into_json()
    else:
        """Lisa please add your modifying netcdf file based on part here"""
        #data = request.json['projection_information'];
        data = request.json['vegetation_map']['0']
        print 'aaaaaaaaaaaaaaaaaaaaaaaaaaa'
        print data
        return