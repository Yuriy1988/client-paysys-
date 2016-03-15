from flask import Response
from app import app, db
from app.models import Transaction, Invoice
from config import CURRENT_API_VERSION


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
    {
        order_id: string,		// {required}
        store_id: string,		// {required}, from $Store
        currency: enum,			// {required}, one of Currency Enum
        items:
        [
            {
                item_id: string,	// {required}
                quantity: integer,	// {required}
                unit_price: decimal	// {required}
            },
            ...
        ]
    }
    < 200 OK $Invoice
    < 400 Bad Request

    """
    
    pass


@app.route('/api/client/{version}/invoices/<invoice_id>'.format(version=CURRENT_API_VERSION), methods=['GET'])
def invoice_info(invoice_id):
    """
    Get invoice info by invoice id.
    """

    pass
