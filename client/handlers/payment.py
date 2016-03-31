from client.handlers.client_utils import mask_card_number, get_store_by_store_id, get_amount, put_to_queue, send_email
from flask import request, jsonify, Response
from client import app, db
from client.models import Invoice, Payment
from client.schemas import PaymentResponceSchema, PaymentRequestSchema
from client.errors import ValidationError, NotFoundError, BaseApiError
from config import CURRENT_CLIENT_SERVER_VERSION
from helper.main import get_route
import json
import datetime


@app.route('/api/client/{version}/invoices/<invoice_id>/payments'.format(
    version=CURRENT_CLIENT_SERVER_VERSION),
    methods=['POST']
)
def payment_create(invoice_id):
    """
    Create invoice using an incoming JSON.

    Test JSON:
    {"card_number": "1111111111111111", "cardholder_name": "John Bowe", "cvv": "111", "expiry_date": "11/1111",
    "notify_by_email": "email@email.com", "notify_by_phone": "1111111111"}

    Returns:
    < 202 Accepted
    {
            id: string,	// payment_id - идентификатор для запроса состояния платежа
            status: string	// статус платежа (default=ACCEPTED - принят в обработку)
    }
    < 400 Bad Request
    < 404 Not Found
    :param invoice_id: Invoice custom (uuid) id.
    """
    # 1. Check if there is an invoice with such id and get is if exists
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError('There is no invoice with such id')

    # 2. Catch JSON with card info
    payment_request_schema = PaymentRequestSchema()
    payment_request_data, payment_request_errors = payment_request_schema.load(request.get_json())

    if payment_request_errors:
        raise ValidationError(errors=payment_request_errors)

    # 3.1. Get merchant_id from Admin (using store API)
    store_json_info = get_store_by_store_id(invoice.store_id)
    store_data = json.loads(store_json_info)

    # 3.2. Get Helper result
    merchant_id = store_data['merchant_id']
    amount = get_amount(invoice.items)
    currency = invoice.currency
    helper_responce = get_route(payment_request_data["paysys_id"], merchant_id, amount, currency)

    # 4.1. Create a JSON for Transaction queue
    transaction_json = json.dumps({
        'invoice': str(invoice),
        'bank_contract': helper_responce['bank_contract'],
        'merchant_contract': helper_responce['merchant_contract'],
        'amount': str(amount * 100),
        'source': payment_request_data
    })

    # 4.2. Send the Transaction JSON to queue
    queue_status = put_to_queue(transaction_json)

    # 5. Save Payment obj to DB
    payment = {
        'payment_account': payment_request_data['payment_account'],
        'status': queue_status["status"],
        'notify_by_email': payment_request_data['notify_by_email'],
        'notify_by_phone': payment_request_data['notify_by_phone'],
        'paysys_id': payment_request_data["paysys_id"],
        'invoice_id': invoice_id
    }
    payment = Payment.create(payment)
    db.session.commit()

    # 6. Create a status JSON for responce
    payment_responce_dict = {
        'id': payment.id,
        'status': payment.status
    }

    # 7. Send an email to user (if user wrote his email in form)
    if payment_request_data['notify_by_email']:
        email_responce = send_email(
            payment_request_data['notify_by_email'],
            "XOPAY transaction status",
            "Thank you for your payment! Transaction status is: {status}".format(status=payment.status)
        )

    payment_responce_schema = PaymentResponceSchema()
    result = payment_responce_schema.dump(payment_responce_dict)

    return jsonify(result.data), 202


@app.route('/api/client/{version}/payment/<payment_id>/status'.format(
    version=CURRENT_CLIENT_SERVER_VERSION),
    methods=['PUT']
)
def payment_update_status(payment_id):
    status = request.get_json()
    if not status:
        raise BaseApiError('No JSON in request')

    payment = Payment.query.get(payment_id)
    if not payment:
        raise NotFoundError('There is no payment with such id')

    try:
        status["status"]
    except:
        raise ValidationError("No 'status' in request JSON")

    payment.status = status["status"]

    payment.updated = datetime.datetime.utcnow()
    db.session.commit()

    return Response(status=200)
