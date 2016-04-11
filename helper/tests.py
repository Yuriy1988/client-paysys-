import unittest
from unittest.mock import MagicMock

import functools
import helper.main
from periphery import admin_api


# Util functions:


def contract_factory(contract_id, commission_fixed, commission_pct):
    return {
        "id": contract_id,
        "commission_fixed": commission_fixed,
        "commission_pct": commission_pct,
        "contract_doc_url": "",
        "filter": "",
        "active": True
    }


def bank_id(route):
    return route["paysys_contract"]["id"]


def merchant_id(route):
    return route["merchant_contract"]["id"]


class TestHelper(unittest.TestCase):

    def setUp(self):
        admin_api.bank_contracts_by_id = MagicMock(
            return_value=[
                contract_factory(1, 3.0, 2.6),
                contract_factory(2, 4.0, 1.8),
                contract_factory(3, 5.0, 1.0),  # min
                contract_factory(4, 0.0, 3.0),  # max
                contract_factory(5, 0.0, 2.8),
            ])
        admin_api.merchant_contracts_by_id = MagicMock(
            return_value=[
                contract_factory(1, 0, 3.1),
                contract_factory(2, 0, 4.0),  # max
                contract_factory(3, 1, 2.8),  # min
            ])
        self.helper_get_route = functools.partial(helper.main.get_route,
                                                  payment_system_id=0,
                                                  merchant_id=0,
                                                  currency='USD'
                                                  )
        self.BANK_ID_ERROR = "Incorrect bank contract are found.\n{}"
        self.MERCHANT_ID_ERROR = "Incorrect merchant contract are found.\n{}"

    def test_zero_amount(self):
        route = self.helper_get_route(amount=0)
        self.assertEqual(bank_id(route), 4, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 3, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_100_amount(self):
        route = self.helper_get_route(amount=100)
        self.assertEqual(bank_id(route), 5, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_1000_amount(self):
        route = self.helper_get_route(amount=1000)
        self.assertEqual(bank_id(route), 3, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))
