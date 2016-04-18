from flask import jsonify

from api import app
from api.models import enum

__author__ = 'Kostel Serhii'


@app.route('/api/client/dev/constants/currency', methods=['GET'])
def constant_currency():
    return jsonify(currency=enum.CURRENCY_ENUM)


@app.route('/api/client/dev/constants/payment_status', methods=['GET'])
def constant_payment_status():
    return jsonify(payment_status=enum.PAYMENT_STATUS_ENUM)
