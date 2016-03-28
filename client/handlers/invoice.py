from flask import Response, request, jsonify, render_template
import json
from flask import request, jsonify, render_template
from client import app, db
from client.models import Invoice, Payment
from client.schemas import InvoiceSchema, VersionSchema
from client.handlers.client_utils import get_store_by_store_id
from config import ROOT, CURRENT_CLIENT_SERVER_VERSION, API_VERSION, BUILD_DATE
from client.errors import NotFoundError, ValidationError

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/', methods=['GET'])
def home():
    invoices = Invoice.query.all()
    if not invoices:
        raise NotFoundError()
    payments = Payment.query.all()
    if not payments:
        raise NotFoundError()
    return render_template('home.html', invoices=invoices, payments=payments)


@app.route('/payment/get_button', methods=['GET'])
def render_get_button():
    create_invoice_url = ROOT + '/api/client/{version}/invoices'.format(version=CURRENT_CLIENT_SERVER_VERSION)
    return render_template('get_button.js', ROOT=ROOT, create_invoice_url=create_invoice_url)


@app.route('/api/client/version', methods=['GET'])
def get_version():
    """
    Return a current server and API versions.
    """
    responce = {
        "api_version": API_VERSION,
        "server_version": CURRENT_CLIENT_SERVER_VERSION,
        "build_date": BUILD_DATE
    }
    version_schema = VersionSchema()
    result = version_schema.dump(responce)
    return jsonify(result.data)


@app.route('/api/client/{version}/invoices'.format(version=CURRENT_CLIENT_SERVER_VERSION), methods=['OPTIONS'])
@crossdomain(origin="*", headers=["Content-Type"])
def invoice_create_options():
    return Response(status=200)


@app.route('/api/client/{version}/invoices'.format(version=CURRENT_CLIENT_SERVER_VERSION), methods=['POST'])
@crossdomain(origin="*", headers=["Content-Type"])
def invoice_create():
    """
    Create invoice using an incoming JSON.

    Test JSON:
    {"order_id": "order_id_1", "store_id": "dss9-asdf-sasf-fsaa", "currency": "USD", "items": [{"store_item_id": "item_id_1",
    "quantity": 3, "unit_price": 23.5}, {"store_item_id": "item_id_2", "quantity": 1, "unit_price": 10}]}

    Returns:
    < 200 OK $Invoice
    < 400 Bad Request

    """
    schema = InvoiceSchema()
    data, errors = schema.load(request.get_json())
    if errors:
        return jsonify(errors=errors), 400

    # Creating a new Invoice object:
    invoice = Invoice.create(data)
    db.session.commit()

    result = schema.dump(invoice)
    return jsonify(result.data)


@app.route('/api/client/{version}/invoices/<invoice_id>'.format(version=CURRENT_CLIENT_SERVER_VERSION), methods=['GET'])
def invoice_get_info(invoice_id):
    """
    Get invoice info by invoice id.

    Returns:
    < 200 OK $Invoice
    < 404 Not Found
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError()

    schema = InvoiceSchema()

    result = schema.dump(invoice)
    return jsonify(result.data)


@app.route('/payment/<invoice_id>', methods=['GET'])
def get_payment_form(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError()

    # Getting custom layout store info from Admin (logo, etc):
    store_json_info = get_store_by_store_id(invoice.store_id)
    if not store_json_info:
        raise NotFoundError

    store_data = json.loads(store_json_info.text)

    store_info = {
        'store_name': store_data['store_name'],
        'store_url': store_data['store_url'],
        'description': store_data['description'],
        'logo': store_data['logo'],
        'show_logo': store_data['show_logo']
    }

    return render_template('payment_form.html',
                           store_info=store_info)


