from flask_restful import Resource
from ubertool.ubertool.kabam import kabam_exe as kabam
from flask import request, jsonify
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class KabamHandler(Resource):
    def __init__(self):
        self.name = "kabam"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return kabam.KabamInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return kabam.KabamOutputs()


class KabamGet(KabamHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Kabam get handler.
        :param jobId: (format = %Y%m%d%H%M%S%f) (15 digits)
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class KabamPost(KabamHandler):

    def post(self, jobId="000000100000011"):
        """
        Kabam post handler.
        :param jobId:
        :return:
        """

        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            data = rest_model_caller.model_run(self.name, jobId, inputs, module=kabam)
            return jsonify(**data)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
