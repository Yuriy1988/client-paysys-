from helper.helper_utils import min_tax_contract, max_tax_contract
from periphery import admin_api


def get_route(payment_system_id, merchant_id, amount, currency):
    """
    Gives the most profitable payment route: couple of contracts.
    Returns dictionary in format:
    {"bank_contract":  $BankContract[Cleaned_up*], "merchant_contract": $MerchantContract[Cleaned_up*]}. (see doc)
    * cleaned up means deleting 'contract_doc_url', 'filter', 'active' fields from contract.
    :param payment_system_id: Id of payment system (payment interface provider)
    :param merchant_id: Id of merchant (payment destination)
    :param amount: Payment amount.
    :param currency: Payment currency.
    """
    # get contracts from admin server via API
    bank_contracts = admin_api.bank_contracts_by_id(payment_system_id, currency)     # -
    merchant_contracts = admin_api.merchant_contracts_by_id(merchant_id, currency)   # +

    # find most profitable deals (contracts)
    paysys_contract = min_tax_contract(bank_contracts, amount)
    merchant_contract = max_tax_contract(merchant_contracts, amount)

    return {
        "paysys_contract": clean_up(paysys_contract),
        "merchant_contract": clean_up(merchant_contract)
    }


def clean_up(contract):
    """Deletes processing useless fields from contract."""
    del contract["contract_doc_url"]
    del contract["filter"]
    del contract["active"]
    return contract
