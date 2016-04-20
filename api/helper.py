from collections import namedtuple
from decimal import Decimal
from api import services

Route = namedtuple('Route', ['paysys_contract', 'merchant_contract'])


def calculate_contract_tax(contract, total_price):
    """
    Calculate total contract tax.
    :param dict contract: Contract json object
    :param decimal total_price: Payment total price
    :return decimal: contract tax
    """
    commission_fixed = Decimal(contract.get('commission_fixed', 0))
    commission_pct = Decimal(contract.get('commission_pct', 0))
    return commission_fixed + (total_price * commission_pct) / Decimal(100)


def _clean_up(contract):
    """
    Remove excess fields from contract.
    :param dict contract: contract object
    :return dict: filtered contract object
    """
    return {key: value for key, value in contract.items() if key not in {'contract_doc_url', 'filter', 'active'}}


def get_route(paysys_id, merchant_id, total_price, currency):
    """
    Gives the most profitable payment route as couple of contracts.
    Clean up contracts from excess fields.

    :param str paysys_id: payment system identifier (payment interface provider)
    :param str merchant_id: merchant identifier (payment destination)
    :param decimal total_price: Payment total price.
    :param str currency: Payment currency.
    :return namedtuple: ($PaysysContract[Cleaned_up*], $MerchantContract[Cleaned_up*]) (see doc)
    """
    # get contracts from admin server via API
    paysys_contracts = services.get_payment_system_contracts(paysys_id, currency)   # -
    merchant_contracts = services.get_merchant_contracts(merchant_id, currency)     # +

    # calculate tax for every contracts
    paysys_with_tax = ((contract, calculate_contract_tax(contract, total_price)) for contract in paysys_contracts)
    merchant_with_tax = ((contract, calculate_contract_tax(contract, total_price)) for contract in merchant_contracts)

    # find most profitable deals (contracts)
    paysys_contract, ps_tax = min(paysys_with_tax, key=lambda v: v[1])
    merchant_contract, mr_tax = max(merchant_with_tax, key=lambda v: v[1])

    return Route(paysys_contract=_clean_up(paysys_contract), merchant_contract=_clean_up(merchant_contract))
