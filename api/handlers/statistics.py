from flask import request, jsonify

from api import api_v1, auth
from api.models import Invoice, Payment
from api.errors import ValidationError
from api.schemas import StatisticsArgsSchema, StatisticsPaymentsSchema


@api_v1.route('/statistics/payments', methods=['GET'])
@auth.auth('system')
def payments_statistics():
    request_schema = StatisticsArgsSchema()
    data, errors = request_schema.load(request.args)
    if errors:
        raise ValidationError(errors=errors)

    query = Payment.query.join(Invoice)

    query = query.filter(Invoice.store_id == data['store_id']) if 'store_id' in data else query
    query = query.filter(Invoice.currency == data['currency']) if 'currency' in data else query
    query = query.filter(Invoice.total_price >= data['from_total_price']) if 'from_total_price' in data else query
    query = query.filter(Invoice.total_price <= data['till_total_price']) if 'till_total_price' in data else query

    query = query.filter(Payment.paysys_id == data['paysys_id']) if 'paysys_id' in data else query
    query = query.filter(Payment.payment_account == data['payment_account']) if 'payment_account' in data else query
    query = query.filter(Payment.status == data['status']) if 'status' in data else query
    query = query.filter(Payment.created >= data['from_date']) if 'from_date' in data else query
    query = query.filter(Payment.updated >= data['till_date']) if 'till_date' in data else query

    order_criterion = getattr(Payment, data['order_by'], getattr(Invoice, data['order_by'], Payment.created))

    query = query.order_by(order_criterion)
    query = query.limit(data['limit'])
    query = query.offset(data['offset'])

    payments = query.all()

    schema = StatisticsPaymentsSchema(many=True)
    result = schema.dump(payments)

    return jsonify(payments=result.data, count=len(payments))
