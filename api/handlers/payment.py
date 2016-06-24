from flask import request, jsonify, redirect, url_for

from api import api_v1, db, auth, utils
from api.errors import ValidationError, NotFoundError
from api.models import Invoice, Payment
from api.schemas import PaymentSchema, PaymentStatusSchema

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
    allowed_paysys = utils.get_allowed_store_paysys(invoice.store_id)
    if data['paysys_id'] not in allowed_paysys:
        raise ValidationError(errors={'paysy_id': ['Current payment system does not allowed to use']})

    data['invoice_id'] = invoice_id
    payment = Payment.create(data)

    # if got an exception - do not save payment into DB
    utils.send_transaction(invoice, payment)

    payment.status = 'ACCEPTED'
    db.session.commit()

    schema = PaymentStatusSchema(exclude=('redirect_url',))
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

    schema = PaymentStatusSchema()
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

    schema = PaymentStatusSchema(partial=True, exclude=('id',))
    data, errors = schema.load(request.get_json(silent=True), origin_model=payment)
    if errors:
        raise ValidationError(errors=errors)

    if data:
        payment.update(data)
        db.session.commit()

    schema = PaymentStatusSchema()
    result = schema.dump(payment)

    return jsonify(result.data)


@api_v1.route('/3d-secure/transaction/<trans_id>/<pay_result>', methods=['GET'])
def transaction_3d_secure_result(trans_id, pay_result):
    """
    Handle redirect from 3D secure server and
    forward result ot the processing.
    Redirect to transaction status page.
    :param trans_id: transaction identifier (equal payment_id and invoice_id)
    :param pay_result: transaction status (success or cancel)
    """
    payment = Payment.query.get(trans_id)
    if not payment:
        raise NotFoundError('There is no payment with such id.')

    extra_info = request.args or {}

    if payment.paysys_id == 'PAY_PAL':
        # Update payment account
        # Prevent recursive 3D secure redirect -> change status to PROCESSED
        payment.payment_account = extra_info.get('payer_id')
        payment.status = 'PROCESSED'
        db.session.commit()

    utils.send_3d_secure_result(trans_id, pay_result, extra_info)

    return redirect(url_for('pages.get_payment_form', invoice_id=trans_id))
