import random
import string
from copy import deepcopy
from unittest.mock import MagicMock
from flask import json
from flask.ext.testing import TestCase

import helper
from api import app, db as app_db, models, transaction
from periphery import admin_api

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
                "unit_price": 23.5
            },
            {
                "store_item_id": "store_item_id_2",
                "quantity": 1,
                "unit_price": 10
            }
        ]
    }

    _card_info = {
        "card_number": "1111111111111111",
        "cardholder_name": "John Bowe",
        "cvv": "111",
        "expiry_date": "11/1111",
        "notify_by_email": "email@email.com",
        "notify_by_phone": "111111111111"
    }

    _payment_request = {
        "paysys_id": "VISA_MASTER",
        "crypted_payment": "ssadadjkfskjashcjkahcu3hd83hdwdh28d283h2e323eu823eufdsjiosjf39u9ejsod0r38u289u28uediweduw",
        "payment_account": "111111******1111",
        "notify_by_email": "email@email.com",
        "notify_by_phone": "111111111111"
    }

    _payment = {
        "card_number": "1111111111111111",
        "notify_by_email": "email@email.com",
        "notify_by_phone": "111111111111",
        "invoice_id": ""  # invoice_id does not exist yet.
    }

    _new_status = {
        "status": "SUCCESS"
    }

    def setUp(self):
        """ Setup before test case """
        app_db.session.close()
        app_db.drop_all()
        app_db.create_all()

        _store = {
            "id": 10,
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

        store_json = _store
        admin_api.get_merchant_account = MagicMock(return_value=_merchant_account)
        admin_api.get_store = MagicMock(return_value=store_json)
        admin_api.check_store_exists = MagicMock(return_value={'exists': True})
        admin_api.get_allowed_store_paysys = MagicMock(return_value=list(models.enum.PAYMENT_SYSTEMS_ID_ENUM))
        admin_api.send_email = MagicMock(return_value=None)
        admin_api.send_sms = MagicMock(return_value=None)
        transaction._push_transaction_to_queue = MagicMock(return_value=None)

        helper.get_route = MagicMock(return_value={
            "paysys_contract": {
                "id": 10,
                "commission_fixed": 10.01,
                "commission_pct": 10,
                "contract_doc_url": "http://www.link10.com",
                "currency": "USD",
                "active": True,
                "filter": "*"
            },
            "merchant_contract": {
                "id": 11,
                "commission_fixed": 11.01,
                "commission_pct": 11,
                "contract_doc_url": "http://www.link11.com",
                "currency": "USD",
                "active": True,
                "filter": "*"
            }
        })

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
        app.config.from_object('config.Testing')
        return app

    @staticmethod
    def rand_int(a=0, b=100):
        return random.randint(a, b)

    @staticmethod
    def rand_str(str_len=5):
        a_zA_Z0_9 = string.ascii_letters + string.digits
        return ''.join((random.choice(a_zA_Z0_9) for i in range(str_len)))

    def get(self, url):
        response = self.client.get(self.api_base + url)
        return response.status_code, response.json

    def post(self, url, body):
        headers = {"Content-Type": "application/json"}
        response = self.client.post(self.api_base + url, data=json.dumps(body), headers=headers)
        return response.status_code, response.json if response.mimetype == 'application/json' else response.data

    def put(self, url, body):
        headers = {"Content-Type": "application/json"}
        response = self.client.put(self.api_base + url, data=json.dumps(body), headers=headers)
        return response.status_code, response.json

    def delete(self, url):
        response = self.client.delete(self.api_base + url)
        return response.status_code, response.json if response.status_code >= 400 else None

    def get_invoice(self):
        return deepcopy(self._invoice)

    def get_payment(self):
        return self._payment.copy()

    def get_card_info(self):
        return self._card_info.copy()

    def get_new_status(self):
        return self._new_status.copy()

    def get_payment_request(self):
        return self._payment_request.copy()
