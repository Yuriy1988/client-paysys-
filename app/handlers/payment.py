from flask import request, jsonify
from app import app, db
from app.models import Invoice, Payment
from app.schemas import VisaMasterSchema, PaymentResponceSchema
from app.errors import ValidationError
from config import CURRENT_API_VERSION


@app.route('/api/client/{version}/invoices/<invoice_id>/payments/visa_master'.format(version=CURRENT_API_VERSION),
           methods=['POST'])
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
    """
    # FIXME: Add a 404-check.
    invoice = Invoice.query.get(invoice_id)

    schema = VisaMasterSchema()
    data, errors = schema.load(request.get_json())

    if errors:
        raise ValidationError(errors=errors)

    # Creating a new Transaction object (for saving to DB):
    data['invoice'] = invoice
    payment = Payment.create(data)
    db.session.commit()

    payment_responce_dict = {
        'id': payment.id,
        'status': 'ACCEPTED'
    }
    payment_responce_schema = PaymentResponceSchema()
    result = payment_responce_schema.dump(payment_responce_dict)

    return jsonify(result.data)
