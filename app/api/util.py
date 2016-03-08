import os
import netCDF4


def add_values_into_json():

    # find path
    app_root = os.path.dirname(os.path.abspath(__file__))
    download_dir = app_root + '/../static/data/'
    file_full_path = download_dir + 'parameter.nc'

    file_handle = netCDF4.Dataset(file_full_path, 'r')

    dimensions = [dimension for dimension in file_handle.dimensions]
    for dimension in dimensions:
        if dimension == 'lat':
            number_of_latitude_values = len(file_handle.dimensions[dimension])
        if dimension == 'lon':
            number_of_longitude_values = len(file_handle.dimensions[dimension])

    latitude_values = file_handle.variables['lat'][:]
    longitude_values = file_handle.variables['lon'][:]
    lower_left_latitude = latitude_values[number_of_latitude_values-1]
    lower_left_longitude = longitude_values[0]
    upper_right_latitude = latitude_values[0]
    upper_right_longitude = longitude_values[number_of_longitude_values-1]

    variables = [variable for variable in file_handle.variables]
    variable_values = file_handle.variables['cov_type'][:,:]
    list_of_variable_values = []

    for i in range(number_of_latitude_values):
        for j in range(len(variable_values[i])):
            list_of_variable_values.append(int(variable_values[i][j]))

    index_of_zero_values = []
    index_of_one_values = []
    index_of_two_values = []
    index_of_three_values = []
    index_of_four_values = []

    for index in [index for index, value in enumerate(list_of_variable_values) if value == 0]:
        index_of_zero_values.append(index)
    for index in [index for index, value in enumerate(list_of_variable_values) if value == 1]:
        index_of_one_values.append(index)
    for index in [index for index, value in enumerate(list_of_variable_values) if value == 2]:
        index_of_two_values.append(index)
    for index in [index for index, value in enumerate(list_of_variable_values) if value == 3]:
        index_of_three_values.append(index)
    for index in [index for index, value in enumerate(list_of_variable_values) if value == 4]:
        index_of_four_values.append(index)

    data = {
              'vegetation_map':
              {
                '0': {
                        'HRU_number': index_of_zero_values
                     },
                '1': {
                        'HRU_number': index_of_one_values
                     },
                '2': {
                        'HRU_number': index_of_two_values
                     },
                '3': {
                        'HRU_number': index_of_three_values
                     },
                '4': {
                        'HRU_number': index_of_four_values
                     }
              },
              'projection_information':
              {
                'ncol': number_of_longitude_values,
                'nrow': number_of_latitude_values,
                'xllcorner': lower_left_longitude,
                'yllcorner': lower_left_latitude,
                'xurcorner': upper_right_longitude,
                'yurcorner': upper_right_latitude,
                'cellsize(m)': 100
              }
            }

    file_handle.close()

    return data


def propagate_single_vegetation_change(original_prms_params, veg_value, hrus):
    """
    Given a PRMS netCDF file, a PRMS vegetation code (0-4), and a list of
    HRU indices that should be changed, update the seven other
    vegetation-dependent parameters.

    Arguments:
        original_prms_params (netCDF4.Dataset): The original parameters file
        veg_value (int): The vegetation value, must be 0, 1, 2, 3, or 4
        hrus (list(int)): List of HRU indices that should get the value given
    """
    assert veg_value in range(5), \
        "PRMS Vegetation Values must be an integer from 0 to 4"

    mod_prms_params = netCDF4.Dataset()

    return mod_prms_params


def propagate_all_vegetation_changes(original_prms_params, vegetation_updates):
    """
    Given a vegetation_updates object and an original_parameters netcdf,
    propagate the updates through the original prms params netcdf and return
    an updated copy of the PRMS parameter netCDF
    """
    return original_prms_params


def get_veg_map_by_hru(prms_params):
    """
    TODO will replace add_values_into_json
    """
    pass
