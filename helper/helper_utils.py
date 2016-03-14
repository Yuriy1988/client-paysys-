import requests
import json


API_URL = "/api/admin/{version}".format(version="dev")


def get_merchant_contracts(merchant_id, currency):
    merchant_contracts_json = requests.get(
        url=API_URL + "/merchants/{merchant_id}/contracts?currency={ccy}".format(merchant_id=merchant_id, ccy=currency)
    )
    return json.loads(merchant_contracts_json).get("merchant_contracts", [])


def get_bank_contracts(payment_system_id, currency):
    bank_contracts_json = requests.get(
        url=API_URL + "/payment_systems/{ps_id}/contracts?currency={ccy}".format(ps_id=payment_system_id, ccy=currency)
    )
    return json.loads(bank_contracts_json).get("bank_contracts", [])


def contract_key_func(amount):
    """
    Return function that finds total tax considering amount (uses for finding max and min tax)
    :param amount: Payment amount
    """
    def get_contract_key(contract):
        return contract.get("fix", 0) + amount * contract.get("percent")
    return get_contract_key


def max_tax_contract(contracts, amount):
    return max(contracts, key=contract_key_func(amount))


def min_tax_contract(contracts, amount):
    return min(contracts, key=contract_key_func(amount))
