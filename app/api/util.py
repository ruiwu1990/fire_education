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
