import random
import string

from antifraud import apis
from copy import deepcopy
from unittest.mock import MagicMock
from flask import json
from flask.ext.testing import TestCase

from api import create_app, db as app_db, auth as api_auth, models, utils

__author__ = 'Andrey Kupriy'


class BaseTestCase(TestCase):

    api_base = '/api/client/dev'

    # defaults
    _invoice = {
        "order_id": "order_id_1",
        "store_id": "00000000-1111-2222-3333-444444444444",
        "currency": "USD",
        "items": [
            {
                "store_item_id": "store_item_id_1",
                "quantity": 3,
                "unit_price": "23.5"
            },
            {
                "store_item_id": "store_item_id_2",
                "quantity": 1,
                "unit_price": "10"
            }
        ]
    }

    _payment = {
        "paysys_id": "VISA_MASTER",
        "crypted_payment": "ssada" * 10,
        "payment_account": "4123987601230000",
        "description": "Test payment",
        "notify_by_email": "email@email.com",
        "notify_by_phone": "380111234567"
    }

    _new_status = {
        "status": "SUCCESS"
    }

    _store = {
        "id": "00000000-1111-2222-3333-444444444444",
        "store_name": "The Greatest Store Ever!",
        "store_url": "http://www.greatest.com",
        "store_identifier": "dss9-asdf-sasf-fsaa",
        "category": None,
        "description": "Desdafggagagagas",
        "logo": None,
        "show_logo": False,
        "merchant_id": "dss9-asdf-sasf-fsda",
        "store_settings":
            {
                "sign_algorithm": "sign_algorithm",
                "sign_key": "somethingdfsfdf",
                "succeed_url": "sdfasdfasfasfsdfasfsdf",
                "failure_url": "sdfasfasfasdfasdfasdfasd",
                "commission_pct": 10.0
            }
        }

    _merchant_account = {
        "bank_name": "Alfa DO Bank",
        "checking_account": "4111111111111111",
        "currency": "USD",
        "mfo": "123456",
        "okpo": "12345678"
    }

    _paysys_contracts = [{
        "id": 10,
        "commission_fixed": 10.01,
        "commission_pct": 10,
        "contract_doc_url": "http://www.link10.com",
        "currency": "USD",
        "active": True,
        "filter": "*"
    }]

    _merchant_contracts = [{
        "id": 11,
        "commission_fixed": 11.01,
        "commission_pct": 11,
        "contract_doc_url": "http://www.link11.com",
        "currency": "USD",
        "active": True,
        "filter": "*"
    }]

    def setUp(self):
        """ Setup before test case """
        app_db.session.close()
        app_db.drop_all()
        app_db.create_all()

        utils.get_store = MagicMock(return_value=self._store.copy())
        utils.check_store_exists = MagicMock(return_value={'exists': True})
        utils.get_allowed_store_paysys = MagicMock(return_value=list(models.enum.PAYMENT_SYSTEMS_ID_ENUM))
        utils.get_merchant_account = MagicMock(return_value=self._merchant_account.copy())
        utils.get_payment_system_contracts = MagicMock(return_value=self._paysys_contracts)
        utils.get_merchant_contracts = MagicMock(return_value=self._merchant_contracts)
        utils.push_to_queue = MagicMock(return_value=None)
        utils.get_merchant_stores = MagicMock(return_value=[self._store.copy()])
        utils.get_antifraud_settings = MagicMock(return_value=[
            {"decline_threshold": '100.00', "three_d_secure_threshold": '30.00'}
        ])
        utils.get_scoring_rules = MagicMock(return_value=[
            {"id": "is_trust_location", "score": 10.0, "parameters": {}},
            {"id": "is_normal_amount", "score": 10.0, "parameters": {"threshold": 200}},
            {"id": "is_normal_count", "score": 10.0, "parameters": {"threshold": 200}},
        ])

        apis.get_country_code_by_ip = MagicMock(return_value={"country_code": "US"})
        apis.get_country_code_by_bin = MagicMock(return_value={"countrycode": "US"})

    def tearDown(self):
        """ Teardown after test case """
        self.db.remove()
        app_db.session.close()
        app_db.drop_all()

    @property
    def db(self):
        """ Database session, that can be used in test """
        return app_db.session

    def create_app(self):
        """ App for testing """
        app = create_app('test')
        return app

    @staticmethod
    def rand_int(a=0, b=100):
        return random.randint(a, b)

    @staticmethod
    def rand_str(str_len=5):
        a_zA_Z0_9 = string.ascii_letters + string.digits
        return ''.join((random.choice(a_zA_Z0_9) for i in range(str_len)))

    def get_system_token(self):
        return api_auth.get_system_token()

    def request(self, url, method='GET', data=None, token=None, **options):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer %s" % token

        data = json.dumps(data) if isinstance(data, dict) else data

        response = self.client.open(self.api_base + url, method=method, data=data, headers=headers, **options)
        body = response.json if response.data and response.mimetype == 'application/json' else response.data
        return response.status_code, body

    def get(self, url, query_args=None, token=None):
        code, body = self.request(url, method='GET', token=token, query_string=query_args or {})
        return code, body

    def post(self, url, body, token=None):
        code, body = self.request(url, method='POST', data=body, token=token)
        return code, body

    def put(self, url, body, token=None):
        code, body = self.request(url, method='PUT', data=body, token=token)
        return code, body

    def delete(self, url, token=None):
        code, body = self.request(url, method='DELETE', token=token)
        return code, body

    def get_invoice(self):
        return deepcopy(self._invoice)

    def get_new_status(self):
        return self._new_status.copy()

    def get_payment(self):
        return self._payment.copy()
