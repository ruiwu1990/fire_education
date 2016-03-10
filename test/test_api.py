"""
Unit tests for server functions contained in app/api/views.py

Author: Matthew A. Turner
Date: 2016-03-10
"""
import json
import os
import unittest

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
        # veg_0_hru_res1 = res1.data['']
        r1_scenario = json.loads(json.loads(res1.data)['scenario'])
        vegmap1_code0 = r1_scenario['veg_map_by_hru']['bare_ground']

        assert vegmap1_code0 == [0, 6, 7, 8, 9, 10]

        # check pulling all scenarios contains the two we've created
        all_scenarios_res = self.client.get('/api/scenarios')

        scenarios_list = all_scenarios_res.data['scenarios']
        assert len(scenarios_list) == 2

        veg_0_hru_res1_all = res1.data['']
        veg_1_hru_res1_all = res1.data['']

        veg_2_hru_res2_all = res2.data['']
        veg_3_hru_res2_all = res2.data['']

        # check pulling single scenarios
        id1 = res1.data['id']
        id2 = res2.data['id']

        res1 = self.client.get('/api/scenarios/' + id1)
        res2 = self.client.get('/api/scenarios/' + id2)



    def test_scenario_delete(self):
        """
        delete an existing scenario by ID
        """
        assert False
