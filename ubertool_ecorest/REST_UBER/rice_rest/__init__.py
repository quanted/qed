from flask_restful import Resource
from ubertool.ubertool.rice import rice_exe as rice
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class RiceHandler(Resource):
    def __init__(self):
        self.name = "rice"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return rice.RiceInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return rice.RiceOutputs()


class RiceGet(RiceHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        RICE get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class RicePost(RiceHandler):

    def post(self, jobId="000000100000011"):
        """
        RICE post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=rice)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
