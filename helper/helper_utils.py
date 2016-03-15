import requests
import json

ADMIN_SERVER_URL = "localhost://"
API_URL = ADMIN_SERVER_URL + "/api/admin/{version}".format(version="dev")


def contract_json_parser(contracts_json):
    contracts = json.loads(contracts_json).get("contracts", [])
    if contracts:
        return contracts
    else:
        raise ValueError("There is no active contracts.")


def get_merchant_contracts(merchant_id, currency):
    contracts_json = requests.get(
        url=API_URL + "/merchants/{merchant_id}/contracts?currency={ccy}&active=true".format(
            merchant_id=merchant_id,
            ccy=currency)
    )
    return contract_json_parser(contracts_json)


def get_bank_contracts(payment_system_id, currency):
    contracts_json = requests.get(
        url=API_URL + "/payment_systems/{ps_id}/contracts?currency={ccy}&active=true".format(
            ps_id=payment_system_id,
            ccy=currency)
    )
    return contract_json_parser(contracts_json)


def contract_key_func(amount):
    """
    Return function that finds total tax considering amount (uses for finding max and min tax)
    :param amount: Payment amount
    """
    def get_contract_key(contract):
        return contract.get("commission_fixed", 0.0) + amount * contract.get("commission_pct", 0.0) / 100.0
    return get_contract_key


def max_tax_contract(contracts, amount):
    return max(contracts, key=contract_key_func(amount))


def min_tax_contract(contracts, amount):
    return min(contracts, key=contract_key_func(amount))
