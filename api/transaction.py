import pika
from pika import exceptions as mq_err
from flask import json

import helper
from api import app, errors, services
from api.schemas import InvoiceSchema

__author__ = 'Kostel Serhii'


# Queue

def _get_queue_connection_parameters():
    """
    Return pika connection parameters object.
    """
    return pika.ConnectionParameters(
        host=app.config["QUEUE_HOST"],
        port=app.config["QUEUE_PORT"],
        virtual_host=app.config["QUEUE_VIRTUAL_HOST"],
        credentials=pika.credentials.PlainCredentials(
            username=app.config["QUEUE_USERNAME"],
            password=app.config["QUEUE_PASSWORD"],
        )
    )


def _push_transaction_to_queue(body_json):
    """
    Open connection with queue,
    declare (pass if already declared) queue name and
    publish body message.

    Declare params:
        durable = True - restore messages after broker reboot
        exclusive = False - multiple connections
        auto_delete = False - do not delete after consumer cancels or disconnects

    Publish properties params:
        delivery_mode = 2 - make message persistent

    :param dict body_json: message to push in queue
    """
    queue = app.config["QUEUE_NAME"]
    body = json.dumps(body_json)
    params = _get_queue_connection_parameters()
    publish_properties = pika.BasicProperties(content_type='text/plain', delivery_mode=2)

    try:

        with pika.BlockingConnection(params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True, exclusive=False, auto_delete=False)
            channel.basic_publish(exchange='', routing_key=queue, body=body, properties=publish_properties)

    except mq_err.AMQPConnectionError as err:
        raise errors.ServiceUnavailable('Queue error: %r' % err)
    except (mq_err.AMQPChannelError, mq_err.AMQPError) as err:
        raise errors.InternalServerError('Queue error: %r' % err)


# Transaction

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
            "paysys_contract": route["paysys_contract"],
            "payment_requisites": {
                "crypted_payment": payment.crypted_payment
            }
        },
        "destination": {
            "merchant_contract": route["merchant_contract"],
            "merchant_account": merchant_account_json
        }
    }

    _push_transaction_to_queue(transaction)
