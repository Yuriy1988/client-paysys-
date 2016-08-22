from sqlalchemy import desc, func
from flask import request, jsonify

from api import api_v1, auth, db
from api.models import Invoice, Payment
from api.errors import ValidationError
from api.schemas import StatisticsArgsSchema, StatisticsPaymentsSchema, StatisticsFilterSchema


def payments_query_filter(query, filters):

    query = query.filter(Invoice.store_id == filters['store_id']) if 'store_id' in filters else query
    query = query.filter(Invoice.currency == filters['currency']) if 'currency' in filters else query
    query = query.filter(Invoice.total_price >= filters['from_total_price']) if 'from_total_price' in filters else query
    query = query.filter(Invoice.total_price <= filters['till_total_price']) if 'till_total_price' in filters else query

    query = query.filter(Payment.paysys_id == filters['paysys_id']) if 'paysys_id' in filters else query
    query = query.filter(Payment.payment_account == filters['payment_account']) if 'payment_account' in filters else query
    query = query.filter(Payment.status == filters['status']) if 'status' in filters else query
    query = query.filter(Payment.created >= filters['from_date']) if 'from_date' in filters else query
    query = query.filter(Payment.created <= filters['till_date']) if 'till_date' in filters else query

    return query


def order_query(query, order_by):
    reverse_order, order_by = order_by[0] == '-', order_by.replace('-', '')
    order_criterion = getattr(Payment, order_by, getattr(Invoice, order_by, Payment.created))
    if reverse_order:
        return query.order_by(desc(order_criterion))
    return query.order_by(order_criterion)


@api_v1.route('/statistics/payments', methods=['GET'])
@auth.auth('system')
def payments_statistics():
    schema = StatisticsArgsSchema()
    data, errors = schema.load(request.args)
    if errors:
        raise ValidationError(errors=errors)

    query = Payment.query.join(Invoice)

    payments_query = payments_query_filter(query, data)

    payments_query = order_query(payments_query, data['order_by'])
    payments_query = payments_query.limit(data['limit'])
    payments_query = payments_query.offset(data['offset'])

    payments = payments_query.all()

    total_count = payments_query_filter(query, data).count()

    schema = StatisticsPaymentsSchema(many=True)
    result = schema.dump(payments)

    return jsonify(payments=result.data, count=len(payments), total_count=total_count)


@api_v1.route('/statistics/payments_count', methods=['GET'])
@auth.auth('system')
def payments_count_statistics():
    schema = StatisticsFilterSchema()
    filters, errors = schema.load(request.args)
    if errors:
        raise ValidationError(errors=errors)

    by = request.args.get('by', 'paysys')

    grouping_options = {
        'paysys': db.session.query(Payment.paysys_id, func.count(Payment.id)).join(Invoice).group_by(Payment.paysys_id),
        'currency': db.session.query(Invoice.currency, func.count(Payment.id)).join(Payment).group_by(Invoice.currency),
        'store': db.session.query(Invoice.store_id, func.count(Payment.id)).join(Payment).group_by(Invoice.store_id),
        'status': db.session.query(Payment.status, func.count(Payment.id)).join(Invoice).group_by(Payment.status),
    }

    if by in grouping_options:
        query = payments_query_filter(grouping_options[by], filters)
    else:
        raise ValidationError(errors="Incorrect value for 'by' parameter.")

    counts = [{"value": value, "count": count} for value, count in query.all()]

    return jsonify(counts=counts)
