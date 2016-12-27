import re
from collections import defaultdict
from REST_UBER.swagger_ui import ApiSpec, Operation, OperationResponses, OperationParameters
from werkzeug.routing import parse_rule
import os
import logging


PROJECT_ROOT = os.environ['PROJECT_ROOT']


def swagger(app):
    output = {
        "swagger": "2.0",
        "info": {
            "title": u"\u00FCbertool API Documentation",
            "description": "Welcome to the EPA's ubertool interactive RESTful API documentation.",
            # "termsOfService": "",
            "contact": {
                "name": u"\u00FCbertool Development Team",
                # "url": "",
                "email": "ubertool-dev@googlegroups.com",
            },
            # "license": {
            #     "name": "",
            #     "url": ""
            # },
            "version": "0.0.1"
        },
        "paths": defaultdict(dict),
        "definitions": defaultdict(dict),
        "tags": []
    }
    paths = output['paths']
    definitions = output['definitions']
    tags = output['tags']

    # TODO: Are these needed (from 'flask_swagger')
    ignore_http_methods = {"HEAD", "OPTIONS"}
    # technically only responses is non-optional
    optional_fields = ['tags', 'consumes', 'produces', 'schemes', 'security',
                       'deprecated', 'operationId', 'externalDocs']

    # Loop over the Flask-RESTful endpoints being served (called "rules"...e.g. /terrplant/)
    for rule in app.url_map.iter_rules():
        endpoint = app.view_functions[rule.endpoint]
        try:
            class_name = endpoint.view_class()
        except AttributeError:
            continue  # skip to next iteration in for-loop ("rule" does not contain an ubertool REST endpoint)
        try:
            inputs = class_name.get_model_inputs().__dict__
            outputs = class_name.get_model_outputs().__dict__
        except AttributeError:
            # This endpoint does not have get_model_inputs() or get_model_outputs()
            logging.exception(AttributeError.message)
            continue  # skip to next iteration, as this is not an ubertool endpoint

        # TODO: Logic for UBERTOOL API ENDPOINTS - Move to separate function for code clarity???
        methods = {}
        for http_method in rule.methods.difference(ignore_http_methods):
            if hasattr(endpoint, 'methods') and http_method in endpoint.methods:
                http_method = http_method.lower()
                methods[http_method] = endpoint.view_class.__dict__.get(http_method)
            else:
                methods[http_method.lower()] = endpoint

        # Extract the Rule argument from URL endpoint (e.g. /<jobId>)
        rule_param = None
        for converter, arguments, variable in parse_rule(str(rule)):  # rule must already be converted to a string
            if converter:
                rule_param = variable

        # Get model name
        model_name = class_name.name
        # Instantiate ApiSpec() class for current endpoint and parse YAML for initial class instance properties
        api_spec = ApiSpec(model_name)

        # This has to be at the end of the for-loop because it converts the 'rule' object to a string
        # Rule = endpoint URL relative to hostname; needs to have special characters escaped to be defaultdict key
        rule = str(rule)
        for arg in re.findall('(<(.*?\:)?(.*?)>)', rule):
            rule = rule.replace(arg[0], '{%s}' % arg[2])

        # For each Rule (endpoint) iterate over its HTTP methods (e.g. POST, GET, PUT, etc...)
        for http_method, handler_method in methods.items():

            if http_method == 'post':

                # Instantiate new Operation class
                operation = Operation()

                # Create Operations object from YAML
                operation.yaml_operation_parse(
                    os.path.join(PROJECT_ROOT, 'REST_UBER', model_name + '_rest', 'apidoc.yaml',),
                    model_name
                )
                api_spec.paths.add_operation(operation)

                # Append Rule parameter name to parameters list if needed
                if rule_param:
                    param = {
                        'in': "path",
                        'name': rule_param,
                        'description': "Job ID for model run",
                        'required': True,
                        "type": "string"
                    }
                    # api_spec.parameters = [param] + api_spec.parameters
                    operation.parameters.insert(0, param)
                    # api_spec.parameters.append(param)

                # Update the 'path' key in the Swagger JSON with the 'operation'
                paths[rule].update({'post': operation.__dict__})

                # Append the 'tag' (top-level) JSON for each rule/endpoint
                tag = api_spec.tags.create_tag(model_name, model_name.capitalize() + ' Model')
                tags.append(tag)

                # TODO: Definitions JSON; move to separate class
                definition_template_inputs = {
                    'type': "object",
                    'properties': {
                        'inputs': {
                            "type": "object",
                            "properties": {}
                        },
                        'run_type': {
                            "type": 'string',
                            "example": "single"
                        }
                    }
                }

                definition_template_outputs = {
                    'type': "object",
                    'properties': {
                        'user_id': {
                            'type': 'string',
                        },
                        'inputs': {
                            # inputs_json
                            'type': 'object',
                            'properties': {}
                        },
                        'outputs': {
                            # outputs_json
                            'type': 'object',
                            'properties': {}
                        },
                        'exp_out': {
                            # exp_out_json
                            'type': 'object',
                            'properties': {}
                        },
                        '_id': {
                            'type': 'string',
                        },
                        'run_type': {
                            'type': 'string',
                        }
                    }
                }

                model_def = {
                    model_name.capitalize() + "Inputs": definition_template_inputs,
                    model_name.capitalize() + "Outputs": definition_template_outputs
                }
                for k, v in inputs.items():
                    # Set the inputs to the input and output definition template
                    model_def[model_name.capitalize() + "Inputs"]['properties']['inputs']['properties'][k] = \
                        model_def[model_name.capitalize() + "Outputs"]['properties']['inputs']['properties'][k] = {
                            "type": "object",
                            "properties": {
                                "0": {
                                    # 'type' is JSON data type (e.g. 'number' is a float; 'string' is a string or binary)
                                    "type": 'string' if str(v.dtype) == 'object' else 'number',
                                    # 'format' is an optional modifier for primitives
                                    "format": 'string' if str(v.dtype) == 'object' else 'float'
                                }
                            }
                    }

                for k, v in outputs.items():
                    # Set the outputs to the output definition template
                    model_def[model_name.capitalize() + "Outputs"]['properties']['outputs']['properties'][k] = {
                        "type": "object",
                        "properties": {
                            "0": {
                                "type": 'string' if str(v.dtype) == 'object' else 'number',
                                "format": 'string' if str(v.dtype) == 'object' else 'float'
                            }
                        }
                    }

                definitions.update(model_def)

            if http_method == 'get':

                # Instantiate new Operation class
                operation = Operation(
                    tags=[model_name],
                    summary="Returns " + model_name.capitalize() + " JSON schema",
                    description="Returns the JSON schema needed by the POST method to run " + model_name.capitalize() +
                                " model",
                    parameters=[],
                    produces=['application/json'],
                    responses=OperationResponses(
                        200,
                        "Returns model input schema required for POST method",
                        schema={
                            "allOf": [
                                {
                                    "$ref": "#/definitions/" + model_name.capitalize() + "Outputs"
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "notes": {
                                            "type": "object",
                                            "properties": {
                                                "info": {'type': 'string'},
                                                "POST": {'type': 'string'},
                                                "GET": {'type': 'string'},
                                                "www": {'type': 'string'}
                                            }
                                        },
                                    }
                                }
                            ]
                        }
                    ).get_json()
                )
                paths[rule].update({'get': operation.__dict__})

    return output
