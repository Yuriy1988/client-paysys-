"""Wraps admin API."""


import json
import requests


ADMIN_API_URL = "http://localhost:7128/api/admin/dev"


def _admin(url, **params):
    return json.loads(requests.get(ADMIN_API_URL + url, params=params).text)


def store_by_id(store_id):
    return _admin("/stores/{}".format(store_id))


def merchant_by_id(merchant_id):
    return _admin("/merchants/{}".format(merchant_id))


def merchant_contracts_by_id(merchant_id, currency):
    return _admin("/payment_systems/{}/contracts".format(merchant_id), currency=currency, active=True)


def bank_contracts_by_id(payment_system_id, currency):
    return _admin("/payment_systems/{}/contracts".format(payment_system_id), currency=currency, active=True)

