from decimal import Decimal


def contract_key_func(total_price):
    """
    Return function that finds total tax considering total_price (uses for finding max and min tax)
    :param total_price: Payment total price
    """
    def get_contract_key(contract):
        return Decimal(contract.get("commission_fixed", 0)) + total_price * Decimal(contract.get("commission_pct", 0)) / Decimal(100)
    return get_contract_key


def max_tax_contract(contracts, total_price):
    return max(contracts, key=contract_key_func(total_price))


def min_tax_contract(contracts, total_price):
    return min(contracts, key=contract_key_func(total_price))


def clean_up(contract):
    """Deletes processing useless fields from contract."""
    del_if_exists(contract, "contract_doc_url")
    del_if_exists(contract, "filter")
    del_if_exists(contract, "active")
    return contract


def del_if_exists(obj, key):
    if key in obj:
        del obj[key]
