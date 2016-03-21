from flask import Response, request, jsonify, render_template
from client import app, db
from client.models import Invoice, Payment
from client.schemas import InvoiceSchema, StoreSchema
from client.handlers.client_utils import get_store_by_store_id
from config import CURRENT_API_VERSION
from client.errors import NotFoundError, ValidationError
from client.forms import VisaMasterPaymentForm


@app.route('/', methods=['GET'])
def home():
    invoices = Invoice.query.all()
    if not invoices:
        raise NotFoundError()
    payments = Payment.query.all()
    if not payments:
        raise NotFoundError()
    return render_template('home.html', invoices=invoices, payments=payments)


@app.route('/api/client/version', methods=['GET'])
def get_version():
    """
    Return a current server version.
    """
    return Response(status=200), CURRENT_API_VERSION


@app.route('/api/client/{version}/invoices'.format(version=CURRENT_API_VERSION), methods=['POST'])
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
        raise ValidationError(errors=errors)

    # Creating a new Invoice object:
    invoice = Invoice.create(data)
    db.session.commit()

    result = schema.dump(invoice)
    return jsonify(result.data)


@app.route('/api/client/{version}/invoices/<invoice_id>'.format(version=CURRENT_API_VERSION), methods=['GET'])
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

    store_schema = StoreSchema()
    store_data, store_errors = store_schema.load(store_json_info)
    if store_errors:
        raise ValidationError(errors=store_errors)
    store_info = {
        'store_name': store_data['store_name'],
        'store_url': store_data['store_url'],
        'description': store_data['description'],
        'logo': store_data['logo'],
        'show_logo': store_data['show_logo']
    }

    # Getting forms:
    visa_master_form = VisaMasterPaymentForm()
    # paypal_form = PayPalForm() TODO: write me.
    # bitcoin_form = BitCoinForm() TODO: write me.

    return render_template('payment_form.html',
                           store_info=store_info,
                           visa_master_form=visa_master_form)


