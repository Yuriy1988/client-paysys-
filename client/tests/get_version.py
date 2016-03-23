from flask import json
import time
import client.handlers
import unittest
from copy import deepcopy
from datetime import datetime


class TestGetVersion(unittest.TestCase):

    _valid_resp = {
            "api_version": "dev",
            "server_version": "dev",
            "build_date": "2016-03-22T18:55:42.768858+00:00"
        }

    def setUp(self):
        self.API_VERSION = 'dev'
        self.CURRENT_CLIENT_SERVER_VERSION = 'dev'
        self.BUILD_DATE = datetime(2016, 3, 22, 18, 55, 42, 768858)
        self.app = client.app.test_client()

    # Tests:

    # GET /api/client/version

    def test_get_valid_responce(self):
        result = self.app.get('/api/client/version')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["api_version"], self._valid_resp["api_version"])
        self.assertEqual(data["server_version"], self._valid_resp["server_version"])
        self.assertEqual(data["build_date"], self._valid_resp["build_date"])
