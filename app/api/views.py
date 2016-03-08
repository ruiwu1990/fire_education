"""
PRMS Fire Modeling API

Date: Feb 25 2016
"""
from datetime import datetime

from flask import jsonify, request, Response
from flask import current_app as app

import json

from . import api
from ..models import Scenario, Hydrograph, VegetationMapByHRU, Inputs, Outputs
from util import (add_values_into_json,
                  propagate_all_vegetation_changes,
                  get_veg_map_by_hru)



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

        scenarios = Scenario.objects.get()

        return jsonify(scenarios=scenarios)

    else:
        BASE_PARAMETER_NC = app.config['BASE_PARAMETER_NC']

        # assemble parts of a new scenario record
        vegetation_updates = json.dumps(request.json['vegetation_updates'])

        name = request.json['name']

        time_received = datetime.now()

        updated_parameter_nc = propagate_all_vegetation_changes(
            BASE_PARAMETER_NC, vegetation_updates
        )

        updated_vegetation_map = get_veg_map_by_hru(updated_parameter_nc)
        veg_map_by_hru = VegetationMapByHRU.from_json(updated_vegetation_map)

        # TODO placeholder
        time_finished = datetime.now()

        # TODO placeholder
        inputs = Inputs()

        # TODO placeholder
        outputs = Outputs()

        # TODO placeholder
        hydrograph = Hydrograph(
            time_array=[datetime(2010, 10, 1, 0), datetime(2010, 10, 1, 1),
                        datetime(2010, 10, 1, 2), datetime(2010, 10, 1, 3)],
            streamflow_array=[24.4, 34.6, 10.0, 86.0]
        )

        new_scenario = Scenario.from_json(
            name=name,
            time_received=time_received,
            time_finished=time_finished,
            veg_map_by_hru=veg_map_by_hru,
            inputs=inputs,
            outputs=outputs,
            hydrograph=hydrograph
        )

        return jsonify(new_scenario.to_json())


@api.route('/api/base-veg-map', methods=['GET'])
def hru_veg_json():
    if request.method == 'GET':
        """generate json file from netcdf file"""
        return jsonify(add_values_into_json())
