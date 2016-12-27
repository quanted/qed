from flask_restful import Resource
from ubertool.ubertool.therps import therps_exe as therps
from flask import request, jsonify
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class TherpsHandler(Resource):
    def __init__(self):
        self.name = "therps"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return therps.TherpsInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return therps.TherpsOutputs()


class TherpsGet(TherpsHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Therps get handler.
        :param jobId: (format = %Y%m%d%H%M%S%f) (15 digits)
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class TherpsPost(TherpsHandler):

    def post(self, jobId="000000100000011"):
        """
        Therps post handler.
        :param jobId:
        :return:
        """

        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            data = rest_model_caller.model_run(self.name, jobId, inputs, module=therps)
            return jsonify(**data)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
