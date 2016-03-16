from flask import Response, request, jsonify
from app import app, db
from app.models import Invoice
from app.schemas import InvoiceSchema
from config import CURRENT_API_VERSION
from app.errors import NotFoundError, ValidationError


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
    {"order_id": "order_id_1", "store_id": "dss9-asdf-sasf-fsaa", "currency": "USD", "items": [{"item_id": "item_id_1",
    "quantity": 3, "unit_price": 23.5}, {"item_id": "item_id_2", "quantity": 1, "unit_price": 10},]}

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
