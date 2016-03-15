from helper.helper_utils import get_merchant_contracts, get_bank_contracts, min_tax_contract, max_tax_contract


def get_route(payment_system_id, merchant_id, amount, currency):
    """
    Gives the most profitable payment route: couple of contracts.
Returns dictionary in format: {"bank_contract": $BankContract, "merchant_contract": $MerchantContract}. (see doc)
    :param payment_system_id: Id of payment system (payment interface provider)
    :param merchant_id: Id of merchant (payment destination)
    :param amount: Payment amount.
    :param currency: Payment currency.
    """
    # get contracts from admin server via API
    bank_contracts = get_bank_contracts(payment_system_id, currency)     # -
    merchant_contracts = get_merchant_contracts(merchant_id, currency)   # +

    # find most profitable deals (contracts)
    bank_contract = min_tax_contract(bank_contracts, amount)
    merchant_contract = max_tax_contract(merchant_contracts, amount)

    return {
        "bank_contract": bank_contract,
        "merchant_contract": merchant_contract
    }
