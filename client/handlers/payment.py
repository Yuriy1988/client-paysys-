from client.handlers.client_utils import mask_card_number, get_store_by_store_id, get_amount, \
    make_transaction_json, put_to_queue
from flask import request, jsonify
from client import app, db
from client.models import Invoice, Payment
from client.schemas import VisaMasterSchema, PaymentResponceSchema, StoreSchema
from client.errors import ValidationError, NotFoundError
from config import CURRENT_API_VERSION
from helper.main import get_route
import json


@app.route('/api/client/{version}/invoices/<invoice_id>/payments/visa_master'.format(
    version=CURRENT_API_VERSION),
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
    # 1. Catch JSON with card info
    visa_master_schema = VisaMasterSchema()
    visa_master_data, visa_master_errors = visa_master_schema.load(request.get_json())

    if visa_master_errors:
        raise ValidationError(errors=visa_master_errors)

    # 2. Save Payment obj to DB
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError()

    payment = {
        'card_number': mask_card_number(visa_master_data['card_number']),
        'status': None,
        'notify_by_email': visa_master_data['notify_by_email'],
        'notify_by_phone': visa_master_data['notify_by_phone'],
        'invoice_id': invoice.id
    }
    payment = Payment.create(payment)
    db.session.commit()

    # 3.1 Get merchant_id from Admin (using store API)
    store_json_info = get_store_by_store_id(invoice.store_id)
    store_data = json.loads(store_json_info)

    # 3.2 Get Helper result
    merchant_id = store_data['merchant_id']
    amount = get_amount(invoice.items)
    currency = invoice.currency
    helper_responce = get_route('VISA_MASTER', merchant_id, amount, currency)

    # 4. Send the Transaction JSON to queue
    transaction_json = make_transaction_json(invoice,
                                            helper_responce['bank_contract'],
                                            helper_responce['merchant_contract'],
                                            amount,
                                            visa_master_data)

    queue_status = put_to_queue(transaction_json)

    # 5. Write payment status to DB
    payment.status = queue_status["status"]
    db.session.commit()

    # 6. Return a status JSON to client
    payment_responce_dict = {
        'id': payment.id,
        'status': payment.status
    }

    payment_responce_schema = PaymentResponceSchema()
    result = payment_responce_schema.dump(payment_responce_dict)

    return jsonify(result.data)
