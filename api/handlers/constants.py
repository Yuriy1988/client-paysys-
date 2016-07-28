from flask import jsonify, current_app as app

from api import api_v1, pages
from api.models import enum

__author__ = 'Kostel Serhii'


# Version

@pages.route('/api/client/version')
def server_version():
    version = {
        'api_version': app.config['CLIENT_API_VERSION'],
        'server_version': app.config['SERVER_VERSION'],
        'build_date': app.config['BUILD_DATE'],
    }
    return jsonify(version)


# Constants
@api_v1.route('/constants/currency', methods=['GET'])
def constant_currency():
    return jsonify(currency=enum.CURRENCY_ENUM)


@api_v1.route('/constants/payment_status', methods=['GET'])
def constant_payment_status():
    return jsonify(payment_status=enum.PAYMENT_STATUS_ENUM)
