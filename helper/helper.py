from helper.helper_utils import get_merchant_contracts, get_bank_contracts, min_tax_contract, max_tax_contract


def get_route(payment_system_id, merchant_id, amount, currency):
    # get contracts from admin server via API
    bank_contracts = get_bank_contracts(payment_system_id, currency)     # -
    merchant_contracts = get_merchant_contracts(merchant_id, currency)   # +

    # find most profitable deals (contracts)
    bank_contract = min_tax_contract(bank_contracts, amount)
    merchant_contract = max_tax_contract(merchant_contracts, amount)

    # do calculations using found contracts
    merchant_amount = amount - merchant_contract.get("fix", 0.0) - amount * merchant_contract.get("percent", 0.0)
    bank_tax = bank_contract.get("fix", 0.0) + amount * bank_contract.get("percent", 0.0)
    profit = merchant_contract.get("fix", 0.0) - bank_contract.get("fix", 0.0)\
        + amount * (merchant_contract.get("percent", 0.0) - bank_contract.get("percent", 0.0))

    return {
        "bank_contract": bank_contract,
        "merchant_contract": merchant_contract,
        "merchant_amount": merchant_amount,
        "bank_tax": bank_tax,
        "profit": profit
    }
