from flask_restful import Resource
from ubertool.ubertool.sip import sip_exe as sip
from flask import request
from REST_UBER import rest_validation, rest_schema, rest_model_caller


class SipHandler(Resource):
    def __init__(self):
        self.name = "sip"

    @staticmethod
    def get_model_inputs():
        """
        Return model's input class.
        :return:
        """
        return sip.SipInputs()

    @staticmethod
    def get_model_outputs():
        """
        Return model's output class.
        :return:
        """
        return sip.SipOutputs()


class SipGet(SipHandler):

    def get(self, jobId="YYYYMMDDHHMMSSuuuuuu"):
        """
        SIP get handler.
        :param jobId:
        :return:
        """
        return rest_schema.get_schema(self.name, jobId)


class SipPost(SipHandler):

    def post(self, jobId="000000100000011"):
        """
        SIP post handler.
        :param jobId:
        :return:
        """
        inputs = rest_validation.parse_inputs(request.json)

        if inputs:
            return rest_model_caller.model_run(self.name, jobId, inputs, module=sip)
        else:
            return rest_model_caller.error(self.name, jobId, inputs)
