"""Wraps admin API."""


import json
import requests

from api import app
from periphery.service_error import handle_service_unavailable_error


@handle_service_unavailable_error(msg="Admin service is unavailable now.")
def _admin(url, **params):
    return json.loads(requests.get(app.config["ADMIN_API_URL"] + url, params=params).text)


def store_by_id(store_id):
    return _admin("/stores/{}".format(store_id))


def merchant_by_id(merchant_id):
    return _admin("/merchants/{}".format(merchant_id))


def merchant_contracts_by_id(merchant_id, currency):
    return _admin("/merchants/{}/contracts".format(merchant_id), currency=currency, active=True)


def bank_contracts_by_id(payment_system_id, currency):
    return _admin("/payment_systems/{}/contracts".format(payment_system_id), currency=currency, active=True)

