from flask import Response, request, jsonify, render_template

from api import app, db
from api.errors import NotFoundError
from api.models import Invoice
from api.schemas import InvoiceSchema
from periphery import admin_api


@app.route('/api/client/dev/invoices', methods=['OPTIONS'])
def invoice_create_options():
    return Response(status=200)


@app.route('/api/client/dev/invoices', methods=['POST'])
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


@app.route('/api/client/dev/invoices/<invoice_id>', methods=['GET'])
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

    result = InvoiceSchema().dump(invoice)
    return jsonify(result.data)


@app.route('/client/payment/<invoice_id>', methods=['GET'])
def get_payment_form(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return render_template('payment_form.html', error='Invoice "%s" not found!' % invoice_id)

    # Getting custom layout store info from Admin (logo, etc):
    store_data = admin_api.store_by_id(invoice.store_id)
    if not store_data:
        return render_template('payment_form.html', error='Store "%s" not found!' % invoice.store_id)

    store_info = {
        'store_name': store_data['store_name'],
        'store_url': store_data['store_url'],
        'description': store_data['description'],
        'logo': store_data['logo'],
        'show_logo': store_data['show_logo']
    }

    invoice_info = {
        'id': invoice.id,
        'amount': invoice.amount,
        'currency': invoice.currency
    }

    return render_template('payment_form.html', store_info=store_info, invoice_info=invoice_info)
