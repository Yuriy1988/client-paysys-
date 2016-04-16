import unittest
from flask import json

from api import app


class TestGetVersion(unittest.TestCase):

    _valid_resp = {
            "api_version": "dev",
            "server_version": "dev",
            "build_date": "2016-01-01T12:00:00+00:00"
        }

    def setUp(self):
        app.config['BUILD_DATE'] = "2016-01-01T12:00:00+00:00"
        self.app = app.test_client()

    # Tests:

    # GET /api/client/version

    def test_get_valid_response(self):
        result = self.app.get('/api/client/version')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["api_version"], self._valid_resp["api_version"])
        self.assertEqual(data["server_version"], self._valid_resp["server_version"])
        self.assertEqual(data["build_date"], self._valid_resp["build_date"])
