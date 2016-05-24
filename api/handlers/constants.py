from flask import jsonify

from api import api_v1
from api.models import enum

__author__ = 'Kostel Serhii'


@api_v1.route('/constants/currency', methods=['GET'])
def constant_currency():
    return jsonify(currency=enum.CURRENCY_ENUM)


@api_v1.route('/constants/payment_status', methods=['GET'])
def constant_payment_status():
    return jsonify(payment_status=enum.PAYMENT_STATUS_ENUM)
