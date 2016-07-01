from antifraud.apis import get_country_code_by_ip, get_country_code_by_bin


def score(payment):
    _score = 0
    if not is_trust_location(payment):
        _score += 0
    if not is_normal_amount(payment):
        _score += 0
    if not is_normal_count(payment):
        _score += 0


def is_trust_location(payment):
    """Country of card  != Country of payer  (get from IP)."""
    # TODO get IP and BIN
    ip = ""
    bin_code = ""
    return get_country_code_by_ip(ip) == get_country_code_by_bin(bin_code)


def is_normal_amount(payment):
    """Amount of payment << or >> average amount of payment for the specific merchant."""
    pass


def is_normal_count(payment):
    """Increasing count of transaction for one merchant."""
    pass
