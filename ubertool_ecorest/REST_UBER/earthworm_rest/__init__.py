from flask_restful import Resource
from ubertool.ubertool.earthworm import earthworm_exe as earthworm
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class EarthwormHandler(Resource):
    def __init__(self):
        self.name = "earthworm"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return earthworm.EarthwormInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return earthworm.EarthwormOutputs()


class EarthwormGet(EarthwormHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        Earthworm get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class EarthwormPost(EarthwormHandler):

    def post(self, jobId="000000100000011"):
        """
        Earthworm post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=earthworm)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
