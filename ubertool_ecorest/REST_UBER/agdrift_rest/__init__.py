from flask_restful import Resource
from ubertool.ubertool.agdrift import agdrift
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class AgdriftHandler(Resource):
    def __init__(self):
        self.name = "agdrift"

    @staticmethod
    def get_model_inputs():
        """
        Return agdrift input class.
        :return:
        """
        return agdrift.AgdriftInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return agdrift output class.
        :return:
        """
        return agdrift.AgdriftOutputs()


class AgdriftGet(AgdriftHandler):

    def get(self, jobId="000000100000011"):
        """
        Agdrift get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class AgdriftPost(AgdriftHandler):

    def post(self, jobId="000000100000011"):
        """
        Agdrift post handler.
        :param jobId:
        :return:
        """

        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=agdrift)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
