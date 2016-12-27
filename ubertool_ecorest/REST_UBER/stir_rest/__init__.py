from flask_restful import Resource
from ubertool.ubertool.stir import stir_exe as stir
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class StirHandler(Resource):
    def __init__(self):
        self.name = "stir"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return stir.StirInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return stir.StirOutputs()


class StirGet(StirHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        STIR get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class StirPost(StirHandler):

    def post(self, jobId="000000100000011"):
        """
        STIR post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=stir)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
