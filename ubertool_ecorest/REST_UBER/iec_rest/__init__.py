from flask_restful import Resource
from ubertool.ubertool.iec import iec_exe as iec
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class IecHandler(Resource):
    def __init__(self):
        self.name = "iec"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return iec.IecInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return iec.IecOutputs()


class IecGet(IecHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        IEC get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class IecPost(IecHandler):

    def post(self, jobId="000000100000011"):
        """
        IEC post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=iec)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
