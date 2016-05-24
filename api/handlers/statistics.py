import decimal
from datetime import timedelta
from flask import request, jsonify

from api import api_v1, db, auth
from api.models import Invoice, Payment
from api.errors import ValidationError
from api.schemas import StatisticsArgsSchema, PaymentSchema


@api_v1.route('/store/<store_id>/statistics', methods=['GET'])
@auth.auth('system')
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
    if 'from_total_price' in data:
        query = query.filter(Invoice.total_price >= decimal.Decimal(data['from_total_price']))
    if 'till_total_price' in data:
        query = query.filter(Invoice.total_price <= decimal.Decimal(data['till_total_price']))

    schema = PaymentSchema(many=True)
    if query.all():
        result = schema.dump(query.all())
    else:
        result = schema.dump(query)
    return jsonify(history=result.data)


# TODO: add to documentation
@api_v1.route('/stores/<store_id>/statistics/autocomplete/payment_id', methods=['GET'])
@auth.auth('system')
def payment_id_autocomplete(store_id):
    search_piece = request.args('payment_id')
    # query = Payment.query.filter(Invoice.store_id == store_id)
    query = db.query(Payment.id).filter(Payment.id.like('%' + search_piece + '%'))
    result = [i for i in query.all()]
    return jsonify(data=result)
