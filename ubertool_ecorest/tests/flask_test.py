import json
from flask_cgi import app
import unittest


class FlaskApiDocsTests(unittest.TestCase):
    """
    All endpoints tested must end with trailing slash "/" or the test will fail during a redirect (Status Code 301).
    This is due to an idiosyncrasy of Flask when dealing with endpoints. If no slash is given, Flask auto redirects to
    endpoint with slash appended to end. This allows for the user to either supply or not supply the trailing slash.
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_apidocs_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_apidocs_version(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/spec/')

        api_json = result.data
        api_dict = json.loads(api_json)
        version = api_dict['info']['version']

        # assert the response data
        self.assertEquals(version, "0.0.1")
