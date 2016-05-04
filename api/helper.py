import re
from collections import namedtuple
from decimal import Decimal

from api import services, errors


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
    print(str(contract.get("name")).ljust(10),
          str(round(commission_fixed, 1)).ljust(10),
          str(round((total_price * commission_pct) / Decimal(100), 1)).ljust(10),
          )
    return commission_fixed + (total_price * commission_pct) / Decimal(100)


def _clean_up(contract):
    """
    Remove excess fields from contract.
    :param dict contract: contract object
    :return dict: filtered contract object
    """
    return {key: value for key, value in contract.items() if key not in {'contract_doc_url', 'filter', 'active'}}


def get_filter(card_number):
    def re_filter(contract):
        filters = contract.get("filter", "*").replace(" ", "").replace("*", ".*").split(",")
        return any(re.compile(f).search(card_number) for f in filters)
    return re_filter


def get_route(paysys_id, merchant_id, total_price, currency, card_number=""):
    """
    Gives the most profitable payment route as couple of contracts.
    Clean up contracts from excess fields.

    :param str paysys_id: payment system identifier (payment interface provider)
    :param str merchant_id: merchant identifier (payment destination)
    :param decimal total_price: Payment total price.
    :param str currency: Payment currency.
    :param card_number: masked card_number for routing
    :return namedtuple: ($PaysysContract[Cleaned_up*], $MerchantContract[Cleaned_up*]) (see doc)
    """
    print("==========================")
    print("for amount:", total_price)
    print("with card number:", card_number)
    print("NAME       FIX        PCT")

    # get contracts from admin server via API
    paysys_contracts = services.get_payment_system_contracts(paysys_id, currency)   # -
    if not paysys_contracts:
        raise errors.InternalServerError('Payment System contracts not found.')

    merchant_contracts = services.get_merchant_contracts(merchant_id, currency)     # +
    if not merchant_contracts:
        raise errors.InternalServerError('Merchant contracts not found.')

    # filtering
    if card_number:
        paysys_contracts = filter(get_filter(card_number), paysys_contracts)

    # calculate tax for every contracts
    paysys_with_tax = ((contract, calculate_contract_tax(contract, total_price)) for contract in paysys_contracts)
    merchant_with_tax = ((contract, calculate_contract_tax(contract, total_price)) for contract in merchant_contracts)
    # find most profitable deals (contracts)
    print("----------pay-sys---------")
    ps_contract, ps_tax = min(paysys_with_tax, key=lambda v: v[1])
    print('min:', ps_contract, ps_tax)
    print("--------------------------")
    print("---------merchant---------")
    mr_contract, mr_tax = max(merchant_with_tax, key=lambda v: v[1])
    print('max:', mr_contract, mr_tax)

    return Route(paysys_contract=_clean_up(ps_contract), merchant_contract=_clean_up(mr_contract))
