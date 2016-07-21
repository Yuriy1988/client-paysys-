from datetime import datetime, timedelta
from functools import lru_cache

from antifraud import apis
from api.models import Invoice
from api import utils
from flask import request


def score(invoice, payment):
    s = 0

    if is_trust_location(payment):
        s += 1

    if is_normal_amount(invoice):
        s += 1

    if is_normal_amount(invoice):
        s += 1

    return s


def is_trust_location(payment):
    """Country of card  != Country of payer  (get from IP)."""
    ip = request.remote_addr
    if not payment.payment_account:
        return True
    bin_code = payment.payment_account[:6]  # get BIN from masked card number
    if not bin_code.isnumeric():
        return
    return apis.get_country_code_by_ip(ip) == apis.get_country_code_by_bin(bin_code) is not None


K = 2  # threshold coefficient of acceleration


def is_normal_amount(invoice):
    """Amount of payment << or >> average amount of payment for the specific merchant."""
    last_30_days_invoices = _get_related_invoices(invoice, 30)
    last_day_invoices = _get_related_invoices(invoice, 1)

    amount_30 = sum(map(lambda i: i.total_price, last_30_days_invoices))
    amount_1 = sum(map(lambda i: i.total_price, last_day_invoices))

    return (amount_30 / 30) * K > amount_1


def is_normal_count(invoice):
    """Increasing count of transaction for one merchant."""
    last_30_days_invoices = _get_related_invoices(invoice, 30)
    last_day_invoices = _get_related_invoices(invoice, 1)

    count_30 = len(last_30_days_invoices)
    count_1 = len(last_day_invoices)

    return (count_30 / 30) * K < count_1


@lru_cache()
def _get_related_invoices(invoice, days):
    merchant_id = utils.get_store(invoice.store_id).get("merchant_id")
    stores = utils.get_merchant_stores(merchant_id)

    invoices = []
    for store in stores:
        invoices.extend(
            Invoice.query.filter(Invoice.store_id == store["id"], Invoice.created > datetime.now() - timedelta(days=days)).all()
        )

    return invoices
