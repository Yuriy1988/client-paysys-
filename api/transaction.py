from api import app, services, helper
from api.message_queue import push_to_queue
from api.schemas import InvoiceSchema

__author__ = 'Kostel Serhii'


def send_transaction(invoice, payment):
    """
    Collect all necessary information about transaction
    and send this object to queue.
    :param invoice: Invoice model instance
    :param payment: Payment model instance
    """
    invoice_json = InvoiceSchema().dump(invoice)

    store = services.get_store(invoice.store_id)
    merchant_id = store['merchant_id']
    merchant_account_json = services.get_merchant_account(merchant_id)

    route = helper.get_route(payment.paysys_id, merchant_id, invoice.total_price, invoice.currency)

    transaction = {
        "id": payment.id,
        "payment": {
            "description": "Payment for order {id}".format(id=invoice.order_id),
            "invoice": invoice_json,
            "amount_coins": invoice.total_price_coins,
        },
        "source": {
            "paysys_contract": route.paysys_contract,
            "payment_requisites": {
                "crypted_payment": payment.crypted_payment
            }
        },
        "destination": {
            "merchant_contract": route.merchant_contract,
            "merchant_account": merchant_account_json
        }
    }

    push_to_queue(app.config['QUEUE_TRANS_FOR_PROCESSING'], transaction)
