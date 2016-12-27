import yaml


class ApiSpec(object):
    def __init__(self, model):
        """
        Provides the API documentation JSON for Swagger UI front end.  Swagger JSON specifications can be found
        at: http://swagger.io/specification
        """

        self.model = model
        self.paths = PathOperations()
        self.tags = Tags()


class PathOperations(object):
    # TODO: Is this class needed?
    def __init__(self):
        """
        PathOperations Object representing an endpoint.  Each PathOperations object must have at least one 'operation' object, which
        represents the HTTP method associated with that path.
        """

        self.operations = {}

    def add_operation(self, operation):
        # TODO: Is this needed?
        """

        :param operation: dict, Operation class represented as dictionary
        """
        operation_dict = operation.__dict__
        self.operations.update(operation_dict)


class Operation(object):
    def __init__(self, tags=[], summary="", description="", consumes=[], produces=[], parameters=[], responses={}):

        """
        Operation Object
        :param method: string, HTTP method in lower case (e.g. get, post, put, delete, etc...)
        :param model_name: string, model name in lower case
        """
        if type(tags) is list:
            self.tags = tags
        else:
            raise TypeError
        if type(summary) is str:
            self.summary = summary
        else:
            raise TypeError
        if type(description) is str:
            self.description = description
        else:
            raise TypeError
        if type(consumes) is list:
            self.consumes = consumes
        else:
            raise TypeError
        if type(produces) is list:
            self.produces = produces
        else:
            raise TypeError
        if type(parameters) is list:
            self.parameters = parameters
        else:
            raise TypeError
        if type(responses) is dict:
            self.responses = responses
        else:
            raise TypeError

    def yaml_operation_parse(self, path_to_yaml, schema_name):
        """
        Parse YAML containing the Swagger information for an operation
        :param schema_name: string, name of Schema Object in the Definitions Object representing the Operation schema
        :param path_to_yaml: string, absolute path to YAML file containing Swagger Operation details
        """

        # TODO: Add validation logic for YAML

        with open(path_to_yaml, 'r') as f:
            api_doc = yaml.load(f)

        self.tags = []
        self.summary = api_doc['summary']
        self.description = api_doc['description']
        if self.valid_content_type(api_doc['consumes']):
            self.consumes = api_doc['consumes']
        if self.valid_content_type(api_doc['produces']):
            self.produces = api_doc['produces']
        self.parameters = api_doc['parameters']
        self.responses = api_doc['responses']

        # TODO: Make sure all operation parameters have been filled with valid values

        self.yaml_operation_update(schema_name)

    def valid_content_type(self, content_type):
        # TODO: Add more content types
        # http://swagger.io/specification/#mimeTypes
        _valid_content_types = ("application/json", "application/xml")
        if content_type in _valid_content_types:
            return True

    def yaml_operation_update(self, schema_name):

        self.tags.append(schema_name)

        # Iterate over 'parameters' in YAML
        for i, param in enumerate(self.parameters):
            if 'schema' in param:
                # If 'parameters' in YAML contains the 'schema' key, use it
                # TODO: Add custom schema AND validate its format
                pass
            else:
                # If no 'schema' key present in YAML 'parameters', use default of response 'body'
                if not schema_name.istitle():  # Convert string to Title Case
                    schema_name = schema_name.capitalize()
                self.parameters[i]['schema'] = {'$ref': '#/definitions/' + schema_name + 'Inputs'}
                # TODO: Make 'in' and 'name' descriptors generic
                self.parameters[i]['in'] = 'body'
                self.parameters[i]['name'] = 'body'

        # Iterate over 'responses' in YAML
        for code, desc in self.responses.items():
            if 'schema' in desc:
                # If 'responses' in YAML contains the 'schema' key, use it
                # TODO: Add custom schema AND validate its format
                pass
            else:
                # If no 'schema' key present in YAML 'parameters', use default of response 'body'
                if not schema_name.istitle():  # Convert string to Title Case
                    schema_name = schema_name.capitalize()
                self.responses[code]['schema'] = {'$ref': '#/definitions/' + schema_name + 'Outputs'}

    def get_json(self):
        return dict(
            tags=self.tags,
            summary=self.summary,
            description=self.description,
            consumes=self.consumes,
            produces=self.produces,
            parameters=self.parameters,
            responses=self.responses
        )


# TODO: Update this for other "in"s (e.g. Form Inputs)
class OperationParameters(object):
    def __init__(self):
        self.json = {
            'in': "body",
            'name': "body",
            'description': "",
            'required': True,
            'schema': {
                "$ref": "#/"
            }
        }

    def update(self, desc="", required=True, definition="#/"):
        self.json['description'] = desc
        self.json['required'] = required
        self.json['schema']['$ref'] = definition

        return self.json


class OperationResponses(object):
    def __init__(self, return_code, description, schema=None, headers=None):

        self.return_code = return_code
        self.description = description
        self.schema = schema
        self.headers = headers

        # http://www.restapitutorial.com/httpstatuscodes.html - Using the Top 10 Response Codes*
        self.codes = {
            "200": "OK",
            "201": "Created",
            "204": "No Content",
            "304": "Not Modified",
            "400": "Bad Request",
            "401": "Unauthorized",
            "403": "Forbidden",
            "404": "Not Found",
            "409": "Conflict",
            "500": "Internal Server Error"
        }

        if not self.valid_code(str(return_code)):
            raise ValueError('Return status code must be: %s' % self.codes.keys())

        if schema is None:
            self.schema = {
                'type': 'object',
                "additionalProperties": {
                    "type": "string"
                }
            }

    def valid_code(self, code):
        if code in self.codes.keys():
            return True

    def get_json(self):
        return {
            self.return_code: {
                'description': self.description,
                'schema': self.schema
            }
        }


class Tags(object):
    # TODO: rename to Tags to represent top-level Swagger JSON (list of tags)
    def __init__(self):

        self.tags = []

    def create_tag(self, model_name, description, external_docs=None):

        tag = dict(
            name=model_name,
            description=description
        )
        if external_docs:
            tag.update(dict(
                externalDocs=external_docs
            ))

        return tag

    def get_tags(self):
        return self.tags
