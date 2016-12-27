from flask_restful import Resource
from ubertool.ubertool.trex import trex_exe as trex
from flask import request, jsonify
from REST_UBER import rest_validation, rest_schema, rest_model_caller
# from REST_UBER.rest_jsonify import jsonify  # Override of Flask `jsonify` method to attempt to handle NumPy arrays


class TrexHandler(Resource):
    def __init__(self):
        self.name = "trex"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return trex.TrexInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return trex.TrexOutputs()


class TrexGet(TrexHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Trex get handler.
        :param jobId: (format = %Y%m%d%H%M%S%f) (15 digits)
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class TrexPost(TrexHandler):

    def post(self, jobId="000000100000011"):
        """
        Trex post handler.
        :param jobId:
        :return:
        """

        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            data = rest_model_caller.model_run(self.name, jobId, inputs, module=trex)
            return jsonify(**data)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
