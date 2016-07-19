from api.tests import base


class TestGetVersion(base.BaseTestCase):

    api_base = ''

    _valid_resp = {
            "api_version": "dev",
            "server_version": "dev",
            # "build_date": "2016-01-01T12:00:00+00:00"
        }

     # Tests:

    # GET /api/client/version

    def test_get_valid_response(self):
        status, body = self.get('/client/version')
        self.assertEqual(status, 200)
        self.assertEqual(body["api_version"], self._valid_resp["api_version"])
        self.assertEqual(body["server_version"], self._valid_resp["server_version"])
        # self.assertEqual(data["build_date"], self._valid_resp["build_date"])
