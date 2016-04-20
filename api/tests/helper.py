import functools
import unittest
from unittest.mock import MagicMock

from api import services, helper


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
    return route.paysys_contract["id"]


def merchant_id(route):
    return route.merchant_contract["id"]


class TestHelper(unittest.TestCase):

    def setUp(self):
        services.get_payment_system_contracts = MagicMock(
            return_value= [
                contract_factory(1, '3.0', '2.6'),
                contract_factory(2, '4.0', '1.8'),
                contract_factory(3, '5.0', '1.0'),  # min
                contract_factory(4, '0.0', '3.0'),  # max
                contract_factory(5, '0.0', '2.8'),
            ])
        services.get_merchant_contracts = MagicMock(
            return_value= [
                contract_factory(1, '0', '3.1'),
                contract_factory(2, '0', '4.0'),  # max
                contract_factory(3, '1', '2.8'),  # min
            ])
        self.helper_get_route = functools.partial(helper.get_route, paysys_id=0, merchant_id=0, currency='USD')

        self.BANK_ID_ERROR = "Incorrect bank contract are found.\n{}"
        self.MERCHANT_ID_ERROR = "Incorrect merchant contract are found.\n{}"

    def test_zero_total_price(self):
        route = self.helper_get_route(total_price=0)
        self.assertEqual(bank_id(route), 4, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 3, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_100_total_price(self):
        route = self.helper_get_route(total_price=100)
        self.assertEqual(bank_id(route), 5, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_1000_total_price(self):
        route = self.helper_get_route(total_price=1000)
        self.assertEqual(bank_id(route), 3, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))
