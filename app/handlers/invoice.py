from flask import Response, request, jsonify, render_template

from app import app, db
from app.models import Invoice
from app.schemas import InvoiceSchema

from config import CURRENT_API_VERSION
from app.errors import NotFoundError, ValidationError
from app.forms import VisaMasterPaymentForm




# Handlers:
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
    "quantity": 3, "unit_price": 23.5}, {"item_id": "item_id_2", "quantity": 1, "unit_price": 10}]}

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


@app.route('/get-payment-form/<paysys_id>/<invoice_id>', methods=['GET'])
def get_payment_form(paysys_id, invoice_id):
    if paysys_id == "VISA_MASTER":
        invoice = Invoice.query.get(invoice_id)

        # Get store info from Admin for custom layout (logo, etc):
        store_info = {
            'logo': 'path_to_logo',
            'name': 'Store Name'
        }
        '''
        url = '{admin_url}/api/admin/{current_api_version}/info/stores/{store_id}/merchant_account'.format(
            admin_url=ADMIN_URL,
            current_api_version=CURRENT_API_VERSION,
            store_id=invoice.store_id
        )
        store_json_info = requests.get(url)
        '''

        form = VisaMasterPaymentForm()
        return render_template('credit_card_form.html',
                               store_info=store_info,
                               form=form)

    elif paysys_id == "PAY_PAL":
        pass

    elif paysys_id == "BIT_COIN":
        pass

    else:
        return 'Wrong paysys_id inside the link'


