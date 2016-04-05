from datetime import timedelta
import decimal
import json

from flask import request, jsonify
from api import app, db
from api.models import Invoice, Payment
from api.errors import ValidationError, NotFoundError, BaseApiError
from config import CURRENT_CLIENT_SERVER_VERSION
from api.schemas import StatisticsArgsSchema, PaymentSchema


def get_amount(items_list):
    amount = 0
    for i in items_list:
        amount += i.quantity * i.unit_price
    return amount


@app.route('/api/client/{version}/store/<store_id>/statistics'.format(
    version=CURRENT_CLIENT_SERVER_VERSION),
    methods=['GET']
)
def get_store_statistics(store_id):
    request_schema = StatisticsArgsSchema()
    data, errors = request_schema.load(request.args)
    if errors:
        raise ValidationError(errors=errors)

    query = Payment.query.filter(Invoice.store_id == store_id)

    if 'payment_id' in data:
        query = query.filter_by(id=data['payment_id'])
    if 'transaction_id' in data:
        query = query.filter_by(transaction_id=data['transaction_id'])
    if 'paysys_id' in data:
        query = query.filter_by(paysys_id=data['paysys_id'])
    if 'status' in data:
        query = query.filter_by(status=data['status'])
    if 'currency' in data:
        query = query.filter(Invoice.currency == data['currency'])
    if 'from_date' in data:
        query = query.filter(Payment.created >= data['from_date'])
    if 'till_date' in data:
        query = query.filter(Payment.updated < data['till_date'] + timedelta(days=1))

    # lists:
    if 'from_amount' in data:
        # query = query.filter(get_amount(Payment.invoice.items) >= decimal.Decimal(data['from_amount']))
        query = [i for i in query if get_amount(i.invoice.items) >= decimal.Decimal(data['from_amount'])]
    if 'till_amount' in data:
        # query = query.filter(get_amount(Payment.invoice.items) <= decimal.Decimal(data['till_amount']))
        query = [ i for i in query if get_amount(i.invoice.items) <= decimal.Decimal(data['till_amount'])]

    schema = PaymentSchema(many=True)
    if query.all():
        result = schema.dump(query.all())
    else:
        result = schema.dump(query)
    return jsonify(history=result.data)


@app.route('/api/client/{version}/<store_id>/statistics/autocomplete/payment_id'.format(
    version=CURRENT_CLIENT_SERVER_VERSION),
    methods=['GET']
)
def payment_id_autocomplete(store_id):
    search_piece = request.args('payment_id')
    # query = Payment.query.filter(Invoice.store_id == store_id)
    query = db.query(Payment.id).filter(Payment.id.like('%' + search_piece + '%'))
    result = [i for i in query.all()]
    return jsonify(data=result)
