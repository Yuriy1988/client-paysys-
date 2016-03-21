import random
import string
import json
from copy import deepcopy

from flask import jsonify
from flask.ext.testing import TestCase

from unittest.mock import MagicMock
import client.handlers.client_utils
from client.schemas import StoreSchema

from client import app, db as app_db

__author__ = 'Andrey Kupriy'


class BaseTestCase(TestCase):
    # If database is missing, run shell command: make db_test_create
    SQLALCHEMY_DATABASE_URI = "postgresql://xopclienttest:test123@localhost/xopclienttestdb"

    api_base = '/api/client/dev'

    # defaults
    _invoice = {
        "order_id": "order_id_1",
        "store_id": "dss9-asdf-sasf-fsaa",
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
        "notify_by_phone": "1111111111"
    }

    _payment = {
        "card_number": "1111111111111111",
        "status": "ACCEPTED",
        "notify_by_email": "email@email.com",
        "notify_by_phone": "011111111111",
        "invoice": _invoice
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

        store_json = json.dumps(_store)

        client.handlers.payment.get_store_by_store_id = MagicMock(return_value=store_json)
        client.handlers.payment.put_to_queue = MagicMock(return_value=["ACCEPTED"])

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
        self.config()
        return app

    def config(self):
        """ Configuration for testing """
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI

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
        return response.status_code, response.json

    def delete(self, url):
        response = self.client.delete(self.api_base + url)
        return response.status_code, response.json if response.status_code >= 400 else None

    def get_invoice(self):
        return deepcopy(self._invoice)

    def get_payment(self):
        return deepcopy(self._payment)

    def get_card_info(self):
        return deepcopy(self._card_info)
