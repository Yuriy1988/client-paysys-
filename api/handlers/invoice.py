from flask import request, jsonify
from flask.ext.cors import cross_origin

from api import app, db
from api.errors import NotFoundError, ValidationError
from api.models import Invoice
from api.schemas import InvoiceSchema
from periphery import admin_api


@app.route('/api/client/dev/invoices', methods=['POST'])
@cross_origin()
def invoice_create():
    """
    Create invoice using an incoming JSON.
    Allow Cross Origin requests.
    """
    schema = InvoiceSchema()
    data, errors = schema.load(request.get_json())
    if errors:
        raise ValidationError(errors=errors)

    store_id = data.get('store_id')
    store_exists = admin_api.store_exists(store_id)
    if not store_exists.get('exists', False):
        raise ValidationError(errors={'store_id': ['Store {store_id} does not exists.'.format(store_id=store_id)]})

    invoice = Invoice.create(data)
    db.session.commit()

    result = schema.dump(invoice)
    return jsonify(result.data)


@app.route('/api/client/dev/invoices/<invoice_id>', methods=['GET'])
def invoice_detail(invoice_id):
    """
    Get invoice detail by invoice id.
    :param str invoice_id: invoice identifier.
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError()

    schema = InvoiceSchema()

    result = schema.dump(invoice)
    return jsonify(result.data)


@app.route('/api/client/dev/invoices/<invoice_id>/invoice_paysys', methods=['GET'])
def invoice_allowed_payment_systems(invoice_id):
    """
    Get list of payment system id, that allowed to pay for invoice.
    :param str invoice_id: invoice identifier.
    """
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFoundError()

    response = admin_api.store_paysys(invoice.store_id)
    store_paysys = response.get('store_paysys', [])
    allowed_invoice_paysys = [sps['paysys_id'] for sps in store_paysys if sps.get('allowed')]

    return jsonify(invoice_paysys=allowed_invoice_paysys)
