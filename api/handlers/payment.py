from flask import request, jsonify

from api import api_v1, db, auth, transaction, services
from api.errors import ValidationError, NotFoundError
from api.models import Invoice, Payment
from api.schemas import PaymentSchema

__author__ = 'Kostel Serhii'


@api_v1.route('/invoices/<invoice_id>/payments', methods=['POST'])
def payment_create(invoice_id):
    """
    Create new payment for invoice.
    :param invoice_id: Invoice identifier.
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError('There is no invoice with such id')

    # Can be only one payment for invoice
    if invoice.payment is not None:
        raise ValidationError('Payment by invoice has been created. Current status: %s' % invoice.payment.status)

    schema = PaymentSchema(exclude=('status',))
    data, errors = schema.load(request.get_json(silent=True))
    if errors:
        raise ValidationError(errors=errors)

    # Allow only payment system, that allowed for payment store.
    allowed_paysys = services.get_allowed_store_paysys(invoice.store_id)
    if data['paysys_id'] not in allowed_paysys:
        raise ValidationError(errors={'paysy_id': ['Current payment system does not allowed to use']})

    data['invoice_id'] = invoice_id
    payment = Payment.create(data)

    # if got an exception - do not save payment into DB
    transaction.send_transaction(invoice, payment)

    payment.status = 'ACCEPTED'
    db.session.commit()

    schema = PaymentSchema(only=('id', 'status',))
    result = schema.dump(payment)

    response = result.data
    response['access_token'] = auth.get_access_token()

    return jsonify(response), 202


@api_v1.route('/payment/<payment_id>', methods=['GET'])
@auth.auth('access_token')
def payment_detail(payment_id):
    """
    Get payment status detail.
    :param payment_id: Payment identifier.
    """
    payment = Payment.query.get(payment_id)
    if not payment:
        raise NotFoundError('There is no payment with such id.')

    schema = PaymentSchema(only=('id', 'status',))
    result = schema.dump(payment)

    return jsonify(result.data)


@api_v1.route('/payment/<payment_id>', methods=['PUT'])
@auth.auth('system')
def payment_update(payment_id):
    """
    Update payment status.
    :param payment_id: Payment identifier.
    """
    payment = Payment.query.get(payment_id)
    if not payment:
        raise NotFoundError('There is no payment with such id.')

    schema = PaymentSchema(partial=True, only=('status',))
    data, errors = schema.load(request.get_json(silent=True), origin_model=payment)
    if errors:
        raise ValidationError(errors=errors)

    if data:
        payment.update(data)
        db.session.commit()

    schema = PaymentSchema(only=('id', 'status',))
    result = schema.dump(payment)

    return jsonify(result.data)
