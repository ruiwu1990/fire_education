"""
Unit tests for server functions contained in app/api/views.py

Author: Matthew A. Turner
Date: 2015-12-12
"""
import json
import unittest

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
                "vegetation_updates": [

                    {
                        "cov_type_code": 0,
                        "HRU_number": [
                            0, 6, 7, 8, 9, 10
                        ]
                    },

                    {
                        "cov_type_code": 1,
                        "HRU_number": [
                            1, 5, 11, 12, 19
                        ]
                    }
                ]
            }
        '''

        raw_data2 = '''
            {
                "name": "test-scenario-2",
                "vegetation_updates": [

                    {
                        "cov_type_code": 2,
                        "HRU_number": [
                            0, 6, 7, 8, 9, 10
                        ]
                    },

                    {
                        "cov_type_code": 3,
                        "HRU_number": [
                            1, 5, 11, 12
                        ]
                    }

                ]
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
        veg_0_hru_res1 = res1.data['']
        veg_1_hru_res1 = res1.data['']

        veg_2_hru_res2 = res2.data['']
        veg_3_hru_res2 = res2.data['']

        assert veg_0_hru_res1 == [0, 6, 7, 8, 9, 10]


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
