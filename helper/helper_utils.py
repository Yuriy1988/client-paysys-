

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


def clean_up(contract):
    """Deletes processing useless fields from contract."""
    del_if_exists(contract, "contract_doc_url")
    del_if_exists(contract, "filter")
    del_if_exists(contract, "active")
    return contract


def del_if_exists(obj, key):
    if key in obj:
        del obj[key]
