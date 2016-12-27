import importlib
import json
import logging
import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
try:
    from flask_cors import CORS
    cors = True
except ImportError:
    cors = False
import pandas as pd

from REST_UBER import terrplant_rest as terrplant
from REST_UBER import sip_rest as sip
from REST_UBER import agdrift_rest as agdrift
from REST_UBER import stir_rest as stir
from REST_UBER import trex_rest as trex
from REST_UBER import therps_rest as therps
from REST_UBER import iec_rest as iec
from REST_UBER import earthworm_rest as earthworm
from REST_UBER import rice_rest as rice
from REST_UBER import kabam_rest as kabam


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})

app = Flask(__name__)
api = Api(app)
if cors:
    CORS(app)
else:
    logging.debug("CORS not enabled")

# TODO: Remove this and Generic model handler below... (not used with refactored models)
_ACTIVE_MODELS = (
    'terrplant',
    'sip',
    'stir',
    'trex',
    'therps',
    'iec',
    'eathworm',
    'rice',
    'sam',
    'kabam'
)
_NO_MODEL_ERROR = "{} model is not available through the REST API"


# TODO: Generic API endpoint (TEMPORARY, remove once all endpoints are explicitly stated)
class ModelCaller(Resource):
    def get(self, model, jid):
        return {'result': 'model=%s, jid=%s' % (model, jid)}

    def post(self, model, jid):
        # TODO: Remove the YAML part of this docstring
        """
        Execute model
        """
        if model in _ACTIVE_MODELS:
            try:
                # Dynamically import the model Python module
                model_module = importlib.import_module('.' + model, model)
                logging.info('============= ' + model)
                # Set the model Object to a local variable (class name = model)
                model_cap = model.capitalize()
                model_object = getattr(model_module, model_cap)
                #logging.info('============= ' + model_object)

                try:
                    run_type = request.json["run_type"]
                    logging.info('============= run_type =' + run_type)
                except KeyError as e:
                    return rest_error_message(e, jid)

                if run_type == "qaqc":
                    logging.info('============= QAQC Run =============')

                    # pd_obj = pd.io.json.read_json(json.dumps(request.json["inputs"]))
                    pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
                    # pd_obj_exp = pd.io.json.read_json(json.dumps(request.json["out_exp"]))
                    pd_obj_exp = pd.DataFrame.from_dict(request.json["out_exp"], dtype='float64')

                    result_json_tuple = model_object(run_type, pd_obj, pd_obj_exp).json

                elif run_type == "batch":
                    logging.info('============= Batch Run =============')
                    # pd_obj = pd.io.json.read_json(json.dumps(request.json["inputs"]))
                    pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')

                    result_json_tuple = model_object(run_type, pd_obj, None).json

                else:
                    logging.info('============= Single Run =============')
                    pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')

                    result_json_tuple = model_object(run_type, pd_obj, None).json

                # Values returned from model run: inputs, outputs, and expected outputs (if QAQC run)
                inputs_json = json.loads(result_json_tuple[0])
                outputs_json = json.loads(result_json_tuple[1])
                exp_out_json = json.loads(result_json_tuple[2])

                return {'user_id': 'admin',
                        'inputs': inputs_json,
                        'outputs': outputs_json,
                        'exp_out': exp_out_json,
                        '_id': jid,
                        'run_type': run_type}

            except Exception as e:
                return rest_error_message(e, jid)
        else:
            return rest_error_message(_NO_MODEL_ERROR.format(model), jid)


def rest_error_message(error, jid):
    """Returns exception error message as valid JSON string to caller
    :param error: Exception, error message
    :param jid: string, job ID
    :return: JSON string
    """
    logging.exception(error)
    e = str(error)
    return json.dumps({'user_id': 'admin', 'result': {'error': e}, '_id': jid})


# TODO: Used for THERPS, is this needed???
class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # or map(int, obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/rest/therps/<jid>', methods=['POST'])
def therps_rest(jid):
    all_result = {}
    try:
        for k, v in request.json.iteritems():
            exec '%s = v' % k
        all_result.setdefault(jid, {}).setdefault('status', 'none')
        from therps import therps
        result = therps.therps(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50,
                                 avian_lc50,
                                 avian_NOAEC, avian_NOAEL,
                                 Species_of_the_tested_bird_avian_ld50,
                                 Species_of_the_tested_bird_avian_lc50,
                                 Species_of_the_tested_bird_avian_NOAEC,
                                 Species_of_the_tested_bird_avian_NOAEL,
                                 bw_avian_ld50, bw_avian_lc50, bw_avian_NOAEC, bw_avian_NOAEL,
                                 mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg,
                                 wp_herp_a_sm,
                                 wp_herp_a_md,
                                 wp_herp_a_lg, c_mamm_a, c_herp_a)
        if (result):
            result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
            # all_result[jid]['status']='done'
            # all_result[jid]['input']=request.json
            # all_result[jid]['result']=result
        return json.dumps({'user_id': 'admin', 'result': result_json, '_id': jid})
    except Exception as e:
        return rest_error_message(e, jid)


@app.route('/rest/kabam/<jid>', methods=['POST'])
def kabam_rest(jid):
    all_result = {}
    try:
        for k, v in request.json.iteritems():
            exec '%s = v' % k
        all_result.setdefault(jid, {}).setdefault('status', 'none')
        from kabam import kabam
        result = kabam.kabam(chemical_name, l_kow, k_oc, c_wdp, water_column_EEC, c_wto,
                                mineau_scaling_factor, x_poc, x_doc, c_ox, w_t, c_ss, oc, k_ow,
                                Species_of_the_tested_bird, bw_quail, bw_duck, bwb_other, avian_ld50,
                                avian_lc50, avian_noaec, m_species, bw_rat, bwm_other, mammalian_ld50,
                                mammalian_lc50, mammalian_chronic_endpoint, lf_p_sediment, lf_p_phytoplankton,
                                lf_p_zooplankton, lf_p_benthic_invertebrates, lf_p_filter_feeders,
                                lf_p_small_fish, lf_p_medium_fish, mf_p_sediment, mf_p_phytoplankton,
                                mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders,
                                mf_p_small_fish, sf_p_sediment, sf_p_phytoplankton, sf_p_zooplankton,
                                sf_p_benthic_invertebrates, sf_p_filter_feeders, ff_p_sediment,
                                ff_p_phytoplankton, ff_p_zooplankton, ff_p_benthic_invertebrates,
                                beninv_p_sediment, beninv_p_phytoplankton, beninv_p_zooplankton, zoo_p_sediment,
                                zoo_p_phyto, s_lipid, s_NLOM, s_water, v_lb_phytoplankton, v_nb_phytoplankton,
                                v_wb_phytoplankton, wb_zoo, v_lb_zoo, v_nb_zoo, v_wb_zoo, wb_beninv,
                                v_lb_beninv, v_nb_beninv, v_wb_beninv, wb_ff, v_lb_ff, v_nb_ff, v_wb_ff, wb_sf,
                                v_lb_sf, v_nb_sf, v_wb_sf, wb_mf, v_lb_mf, v_nb_mf, v_wb_mf, wb_lf, v_lb_lf,
                                v_nb_lf, v_wb_lf, kg_phytoplankton, kd_phytoplankton, ke_phytoplankton,
                                mo_phytoplankton, mp_phytoplankton, km_phytoplankton, km_zoo, k1_phytoplankton,
                                k2_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k1_beninv, k2_beninv,
                                kd_beninv, ke_beninv, km_beninv, k1_ff, k2_ff, kd_ff, ke_ff, km_ff, k1_sf,
                                k2_sf, kd_sf, ke_sf, km_sf, k1_mf, k2_mf, kd_mf, ke_mf, km_mf, k1_lf, k2_lf,
                                kd_lf, ke_lf, km_lf, rate_constants, s_respire, phyto_respire, zoo_respire,
                                beninv_respire, ff_respire, sfish_respire, mfish_respire, lfish_respire)
        if (result):
            result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
            # all_result[jid]['status']='done'
            # all_result[jid]['input']=request.json
            # all_result[jid]['result']=result
            return json.dumps({'user_id': 'admin', 'result': result_json, '_id': jid})
    except Exception as e:
        return rest_error_message(e, jid)


@app.route('/rest/ubertool/sam/<jid>', methods=['POST'])
def sam_rest(jid):
    try:
        import REST_UBER.sam_rest.sam_rest_model as sam

        try:
            post_payload = request.json
            run_type = post_payload["run_type"]
        except KeyError as e:
            return rest_error_message(e, jid)

        if run_type == "qaqc":
            logging.info('============= QAQC Run =============')

        elif run_type == "batch":
            logging.info('============= Batch Run =============')

        else:
            logging.info('============= Single Run =============')
            inputs_json = post_payload["inputs"]

            logging.info(inputs_json)

            result_json_tuple = sam.sam(inputs_json, jid, run_type)

        # Values returned from model run: inputs, outputs, and expected outputs (if QAQC run)
        # inputs_json = json.loads(result_json_tuple[0])
        outputs_json = result_json_tuple
        exp_out_json = ""

        return json.dumps({
            'user_id': 'admin',
            'inputs': inputs_json,
            'outputs': outputs_json,
            'exp_out': exp_out_json,
            '_id': jid,
            'run_type': run_type
        })

    except Exception as e:
        return rest_error_message(e, jid)


# Declare endpoints for each model
# These are the endpoints that will be introspected by the swagger() method & shown on API spec page
# TODO: Add model endpoints here once they are refactored
api.add_resource(terrplant.TerrplantGet, '/rest/ubertool/terrplant/')
api.add_resource(terrplant.TerrplantPost, '/rest/ubertool/terrplant/<string:jobId>')
api.add_resource(sip.SipGet, '/rest/ubertool/sip/')
api.add_resource(sip.SipPost, '/rest/ubertool/sip/<string:jobId>')
api.add_resource(agdrift.AgdriftGet, '/rest/ubertool/agdrift/')
api.add_resource(agdrift.AgdriftPost, '/rest/ubertool/agdrift/<string:jobId>')
api.add_resource(stir.StirGet, '/rest/ubertool/stir/')
api.add_resource(stir.StirPost, '/rest/ubertool/stir/<string:jobId>')
api.add_resource(trex.TrexGet, '/rest/ubertool/trex/')
api.add_resource(trex.TrexPost, '/rest/ubertool/trex/<string:jobId>')
api.add_resource(therps.TherpsGet, '/rest/ubertool/therps/')
api.add_resource(therps.TherpsPost, '/rest/ubertool/therps/<string:jobId>')
api.add_resource(iec.IecGet, '/rest/ubertool/iec/')
api.add_resource(iec.IecPost, '/rest/ubertool/iec/<string:jobId>')
api.add_resource(earthworm.EarthwormGet, '/rest/ubertool/earthworm/')
api.add_resource(earthworm.EarthwormPost, '/rest/ubertool/earthworm/<string:jobId>')
api.add_resource(rice.RiceGet, '/rest/ubertool/rice/')
api.add_resource(rice.RicePost, '/rest/ubertool/rice/<string:jobId>')
api.add_resource(kabam.KabamGet, '/rest/ubertool/kabam/')
api.add_resource(kabam.KabamPost, '/rest/ubertool/kabam/<string:jobId>')
api.add_resource(ModelCaller, '/rest/ubertool/<string:model>/<string:jid>')  # Temporary generic route for API endpoints


@app.route("/api/spec/")
def spec():
    """
    Route that returns the Swagger formatted JSON representing the Ubertool API.
    :return: Swagger formatted JSON string
    """
    # from flask_swagger import swagger
    from uber_swagger import swagger

    swag = swagger(app)

    # TODO: Use in production and remove 'jsonify' below
    # return json.dumps(
    #     swag,
    #     separators=(',', ':')  # This produces a 'minified' JSON output
    # )

    return jsonify(swag)  # This produces a 'pretty printed' JSON output


@app.route("/api/")
def api_doc():
    """
    Route to serve the API documentation (Swagger UI) static page being served by the backend.
    :return:
    """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""
=============================================================================================
                              O R E  T E S T I N G
=============================================================================================
"""


@app.route('/ore/load/<query>', methods=['GET'])
def ore_rest_load_query(query):
    """
    Endpoint returns the list of Crops to populate the Crop-Target Category Lookup tab
    :param query:
    :return:
    """
    from REST_UBER.ore_rest import ore_db
    # print query

    result = ore_db.loadChoices(query)

    return json.dumps({"result": result})


@app.route('/ore/category', methods=['POST'])
def ore_rest_category_query():
    """
    Endpoint for populating the exposure scenario tab. OnPageLoad: based on the default crop target category.
    :return: JSON string
    """
    from REST_UBER.ore_rest import ore_db

    query = {}
    for k, v in request.json.iteritems():
        exec "query['%s'] = v" % k
        # print k, v

    result = ore_db.oreWorkerActivities(query)

    return json.dumps({"result": result})


@app.route('/ore/output', methods=['POST'])
def ore_rest_output_query():
    """
    Endpoint for running the ORCA calculations on a user-set exposure scenario and returning the model output
    :return: JSON string
    """
    from REST_UBER.ore_rest import ore_db, ore_rest_model
    inputs = request.json

    # query = {}
    # for k, v in request.json.iteritems():
    #     exec "query['%s'] = v" % k
    #     # print k, v

    query_result_list = ore_db.oreOutputQuery(inputs)
    output = ore_rest_model.ore(inputs, query_result_list)

    return json.dumps({
        "result": {
                "input": inputs,
                "output": output
        }
    })


if __name__ == '__main__':
    app.run(port=7777, debug=True)  # To run on locahost
    # app.run(host='0.0.0.0', port=7777, debug=True)  # 'host' param needed to expose server publicly w/o NGINX/uWSGI
