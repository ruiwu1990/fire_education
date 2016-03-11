"""
Unit tests for server functions contained in app/api/views.py

Author: Matthew A. Turner
Date: 2016-03-10
"""
import json
import os
import unittest

from datetime import datetime

os.environ['FLASKCONFIG'] = 'testing'

from manage import app


class TestAPI(unittest.TestCase):
    """

    """
    def setUp(self):

        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_scenario_creation(self):
        """
        create and query generation of a scenario: (POST/GET scenarios/ GET sccenarios/{scenarioId})
        """
        # send requests to server that will edit test/data/parameter.nc
        raw_data = '''
            {
                "name": "test-scenario-1",
                "veg_map_by_hru": {
                    "bare_ground": [0, 1, 2, 3, 5, 10, 11],
                    "grasses": [4, 6, 7, 17, 18, 19],
                    "shrubs": [9, 12, 13],
                    "trees": [8, 14, 15, 16],
                    "conifers": []
                }
            }
        '''

        raw_data2 = '''
            {
                "name": "test-scenario-2",
                "veg_map_by_hru": {
                    "bare_ground": [0, 10, 11],
                    "grasses": [2, 3, 5, 7, 17, 18, 19],
                    "shrubs": [9, 12, 13],
                    "trees": [8, 14, 15, 16],
                    "conifers": [4, 6, 1]
                }
            }
        '''

        res1 = self.client.post('/api/scenarios', data=raw_data,
                                headers={
                                   'Content-Type': 'application/json',
                                   'Origin': '*'}
                                )

        res2 = self.client.post('/api/scenarios', data=raw_data2,
                                headers={
                                    'Content-Type': 'application/json',
                                    'Origin': '*'}
                                )

        # check the results from posts above; maps should be updated as follows
        r1_scenario = json.loads(json.loads(res1.data)['scenario'])

        assert r1_scenario['name'] == 'test-scenario-1'

        vegmap1_code0 = r1_scenario['veg_map_by_hru']['bare_ground']
        vegmap1_code1 = r1_scenario['veg_map_by_hru']['grasses']
        vegmap1_code2 = r1_scenario['veg_map_by_hru']['shrubs']
        vegmap1_code3 = r1_scenario['veg_map_by_hru']['trees']
        vegmap1_code4 = r1_scenario['veg_map_by_hru']['conifers']

        # TODO this is just what exists currently in test/data/parameter.nc
        # after John Erickson's updates are worked in, update this
        assert vegmap1_code0 == [0, 1, 2, 10]
        assert vegmap1_code1 == [3,  4,  8,  9, 11, 15, 16, 19]
        assert vegmap1_code2 == [5,  6,  7, 17, 18]
        assert vegmap1_code3 == [12, 13, 14]
        assert vegmap1_code4 == []

        inputs = r1_scenario['inputs']
        expected_inputs = {
            'control': 'http://example.com/control.dat',
            'parameter': 'http://example.com/parameter.nc',
            'data': 'http://example.com/data.nc'
        }
        assert inputs == expected_inputs

        outputs = r1_scenario['outputs']
        expected_outputs = {
            'statvar': 'http://example.com/statvar.nc'
        }
        assert outputs == expected_outputs

        projection_information = \
            r1_scenario['veg_map_by_hru']['projection_information']
        # the ur corner has floats that get mangled; check approx equals
        xurcorner = projection_information['xurcorner']
        yurcorner = projection_information['yurcorner']
        xllcorner = projection_information['xllcorner']
        yllcorner = projection_information['yllcorner']
        expected_xurcorner = 2.9000001
        expected_yurcorner = -5.0999999
        assert abs(xurcorner - expected_xurcorner) < 1e6
        assert abs(yurcorner - expected_yurcorner) < 1e6
        expected_xllcorner = 2.9000001
        expected_yllcorner = -5.0999999
        assert abs(xllcorner - expected_xllcorner) < 1e6
        assert abs(yllcorner - expected_yllcorner) < 1e6
        del projection_information['xurcorner']
        del projection_information['yurcorner']
        del projection_information['xllcorner']
        del projection_information['yllcorner']
        expected_projection_information = dict(
            ncol=5,
            nrow=4,
            cellsize=100
        )
        assert projection_information == expected_projection_information

        hydrograph = r1_scenario['hydrograph']
        time_array = hydrograph['time_array']
        streamflow_array = hydrograph['streamflow_array']
        expected_time_array =[
            '2010-10-01T00:00:00', '2010-10-01T01:00:00',
            '2010-10-01T02:00:00', '2010-10-01T03:00:00'
        ]
        expected_streamflow_array = [24.4, 34.6, 10.0, 86.0]
        assert time_array == expected_time_array
        assert streamflow_array == expected_streamflow_array

        then = datetime.now()
        year = then.year
        month = then.month if then.month >= 10 else '0' + str(then.month)
        day = then.day if then.day >= 10 else '0' + str(then.day)

        expected_time_received_date = "{0}-{1}-{2}".format(year, month, day)
        time_received_date = r1_scenario['time_received'].split('T')[0]
        assert time_received_date == expected_time_received_date

        expected_time_finished_date = "{0}-{1}-{2}".format(year, month, day)
        time_finished_date = r1_scenario['time_finished'].split('T')[0]
        assert time_finished_date == expected_time_finished_date

        # check pulling all scenarios contains the two we've created
        # all_scenarios_res = self.client.get('/api/scenarios', )

        # scenarios_list = all_scenarios_res.data['scenarios']
        # assert len(scenarios_list) == 2

        # # check pulling single scenarios
        # id1 = res1.data['id']
        # id2 = res2.data['id']

        # res1 = self.client.get('/api/scenarios/' + id1)
        # res2 = self.client.get('/api/scenarios/' + id2)


    def test_scenario_delete(self):
        """
        delete an existing scenario by ID
        """
        assert False
