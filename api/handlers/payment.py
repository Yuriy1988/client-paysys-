import datetime

import helper
from api import app, db
from api.errors import ValidationError, NotFoundError, BaseApiError
from api.models import Invoice, Payment
from api.schemas import PaymentSchema, InvoiceSchema
from flask import request, jsonify, Response
from periphery import admin_api, notification_api, queue


@app.route('/api/client/dev/payment/<payment_id>', methods=['PUT'])
def payment_update_status(payment_id):
    status = request.get_json()
    if not status:
        raise BaseApiError('No JSON in request.')
    if "status" not in status:
        raise ValidationError("No 'status' in request JSON.")

    payment = Payment.query.get(payment_id)
    if not payment:
        raise NotFoundError('There is no payment with such id.')

    payment.status = status["status"]

    payment.updated = datetime.datetime.utcnow()
    db.session.commit()

    return Response(status=200)


@app.route('/api/client/dev/invoices/<invoice_id>/payments', methods=['POST'])
def payment_create(invoice_id):
    """
    :param invoice_id: Invoice custom (uuid) id.
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError('There is no invoice with such id')

    payment_request, errors = PaymentSchema().load(request.get_json())
    if errors:
        raise ValidationError(errors=errors)

    payment = process_payment(invoice_id, payment_request)

    queue.push(construct_transaction(payment_request, invoice, payment))

    # payment_request['notify_by_email'] and notify(payment_request['notify_by_email'], payment)

    return jsonify({'id': payment.id, 'status': payment.status}), 202


def construct_transaction(payment_request, invoice, payment):
    serialized_invoice = InvoiceSchema().dump(invoice)
    merchant_id = admin_api.store_by_id(invoice.store_id)["merchant_id"]
    merchant_account = admin_api.merchant_by_id(merchant_id)["merchant_account"]
    route = helper.get_route(payment_request["paysys_id"], merchant_id, invoice.amount, invoice.currency)

    transaction = {
        "id": payment.id,
        "payment": {
            "description": "TODO: description support.",
            "invoice": serialized_invoice,
            "amount_coins": invoice.amount,
        },
        "source": {
            "paysys_contract": route["paysys_contract"],
            "payment_requisites": {
                "crypted_payment": payment_request["crypted_payment"]
            }
        },
        "destination": {
            "merchant_contract": route["merchant_contract"],
            "merchant_account": merchant_account
        }
    }
    # FIXME: add validation.
    # print(TransactionSchema().validate(transaction))
    return transaction


def process_payment(invoice_id, payment_request_data):
    payment = {
        'payment_account': payment_request_data['payment_account'],
        'status': "ACCEPTED",
        'invoice_id': invoice_id,
        'paysys_id': payment_request_data["paysys_id"],
        'notify_by_email': payment_request_data.get('notify_by_email'),
        'notify_by_phone': payment_request_data.get('notify_by_phone'),
    }

    payment = Payment.create(payment)
    db.session.commit()

    return payment


def notify(email, payment):
    return notification_api.send_email(
        email,
        "XOPAY transaction status",
        "Thank you for your payment! Transaction status is: {status}".format(status=payment.status)
    )
