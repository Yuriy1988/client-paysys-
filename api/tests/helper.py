import functools
import unittest
from unittest.mock import MagicMock

from api import utils, helper


# Util functions:


def contract_factory(contract_id, name, commission_fixed, commission_pct, filter="*"):
    return {
        "id": contract_id,
        "name": name,
        "commission_fixed": commission_fixed,
        "commission_pct": commission_pct,
        "contract_doc_url": "",
        "filter": filter,
        "active": True
    }


def bank_id(route):
    return route.paysys_contract["id"]


def merchant_id(route):
    return route.merchant_contract["id"]


class TestHelper(unittest.TestCase):

    def setUp(self):
        utils.get_payment_system_contracts = MagicMock(
            return_value=[
                contract_factory(1, 'visa',       '7.0', '2.5', "4*"),
                contract_factory(2, 'master',     '8.0', '2.3', "5*"),
                contract_factory(3, 'privat all', '0.0', '2.4', "*"),
                contract_factory(4, 'privat',     '0.0', '1.9', "521857*, 516798*"),
                contract_factory(5, 'aval',       '0.0', '2.0', "414951*"),
                contract_factory(6, 'aval all',   '0.0', '2.6', "*"),
                contract_factory(7, 'shved',      '10.0', '2.4', "*"),
            ])
        utils.get_merchant_contracts = MagicMock(
            return_value=[
                contract_factory(1, 'merch1', '0', '3.1'),
                contract_factory(2, 'merch2', '0', '4.0'),  # max
                contract_factory(3, 'merch3', '1', '2.8'),  # min
            ])
        self.helper_get_route = functools.partial(helper.get_route, paysys_id=0, merchant_id=0, currency='USD')

        self.BANK_ID_ERROR = "Incorrect bank contract are found.\n{}"
        self.MERCHANT_ID_ERROR = "Incorrect merchant contract are found.\n{}"

    def test_zero_total_price(self):
        route = self.helper_get_route(total_price=0)
        self.assertEqual(bank_id(route), 3, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 3, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_100_total_price(self):
        route = self.helper_get_route(total_price=100, card_number="414951*****123")
        self.assertEqual(bank_id(route), 5, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_1000_total_price_privat(self):
        route = self.helper_get_route(total_price=1000, card_number="516798*****123")
        self.assertEqual(bank_id(route), 4, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_1000_total_privat_all(self):
        route = self.helper_get_route(total_price=1000, card_number="500000*****123")
        self.assertEqual(bank_id(route), 3, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))

    def test_100000_master(self):
        route = self.helper_get_route(total_price=1000000, card_number="500000*****123")
        self.assertEqual(bank_id(route), 2, msg=self.BANK_ID_ERROR.format(route))
        self.assertEqual(merchant_id(route), 2, msg=self.MERCHANT_ID_ERROR.format(route))
