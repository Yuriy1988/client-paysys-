from flask import request, jsonify, Response

from api import app, db, transaction
from api.errors import ValidationError, NotFoundError
from api.models import Invoice, Payment
from api.schemas import PaymentSchema
from periphery import admin_api, notification_api


@app.route('/api/client/dev/invoices/<invoice_id>/payments', methods=['POST'])
def payment_create(invoice_id):
    """
    Create new payment for invoice.
    :param invoice_id: Invoice identifier.
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError('There is no invoice with such id')

    schema = PaymentSchema(exclude=('status',))
    data, errors = schema.load(request.get_json())
    if errors:
        raise ValidationError(errors=errors)

    # Allow only payment system, that allowed for payment store.
    allowed_paysys = admin_api.get_allowed_store_paysys(invoice.store_id)
    if data['paysys_id'] not in allowed_paysys:
        raise ValidationError(errors={'paysy_id': ['Current payment system does not allowed to use']})

    data['invoice_id'] = invoice_id
    payment = Payment.create(data)

    # if got an exception - do not save payment into DB
    transaction.send_transaction(invoice, payment)

    payment.status = 'ACCEPTED'
    db.session.commit()

    if payment.notify_by_email:
        notification_api.notify(payment.notify_by_email, payment)

    schema = PaymentSchema(only=('id', 'status',))
    result = schema.dump(payment)

    return jsonify(result.data), 202


@app.route('/api/client/dev/payment/<payment_id>', methods=['PUT'])
def payment_update(payment_id):
    """
    Update payment status.
    :param payment_id: Invoice identifier.
    """
    payment = Payment.query.get(payment_id)
    if not payment:
        raise NotFoundError('There is no payment with such id.')

    schema = PaymentSchema(only=('status',))
    data, errors = schema.load(request.get_json())
    if errors:
        raise ValidationError(errors=errors)

    payment.status = data["status"]
    db.session.commit()

    return Response(status=200)
