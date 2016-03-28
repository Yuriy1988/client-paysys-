from datetime import timedelta
from flask import request, jsonify
from client import app
from client.models import Invoice, Payment
from client.errors import ValidationError, NotFoundError, BaseApiError
from config import CURRENT_CLIENT_SERVER_VERSION
from client.schemas import StatisticsArgsSchema, PaymentSchema


@app.route('/api/client/{version}/store/<store_id>/statistics'.format(
    version=CURRENT_CLIENT_SERVER_VERSION),
    methods=['GET']
)
def get_store_statistics(store_id):
    request_schema = StatisticsArgsSchema()
    data, errors = request_schema.load(request.args)
    if errors:
        raise ValidationError(errors=errors)

    query = Payment.query
    if 'payment_id' in data:
        query = query.filter_by(id=data['payment_id'])
    if 'transaction_id' in data:
        query = query.filter_by(transaction_id=data['transaction_id'])
    if 'paysys_id' in data:
        query = query.filter_by(paysys_id=data['paysys_id'])
    if 'status' in data:
        query = query.filter_by(status=data['status'])
    if 'currency' in data:
        query = query.join(Invoice).filter(Invoice.currency == data['currency'])
    if 'from_date' in data:
        query = query.filter(Payment.created >= data['from_date'])
    if 'till_date' in data:
        query = query.filter(Payment.updated < data['till_date'] + timedelta(days=1))

    schema = PaymentSchema(many=True)
    result = schema.dump(query.all())
    return jsonify(history=result.data)
