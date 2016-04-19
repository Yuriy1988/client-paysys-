from flask import jsonify, render_template

from api import app, models
from periphery import admin_api


@app.route('/')
def index():
    """ Redirect from root to admin page """
    return app.send_static_file('client/home.html')


@app.route('/client/demo_shop', methods=['GET'])
def demo_shop():
    """ Demo shop handler """
    return render_template('demo_shop.html')


@app.route('/client/version', methods=['GET'])
def get_version():
    """ Return a current server and API versions """
    response = {
        "api_version": app.config["API_VERSION"],
        "server_version": 'dev',
        "build_date": app.config["BUILD_DATE"]
    }
    return jsonify(response)


@app.route('/client/payment/<invoice_id>', methods=['GET'])
def get_payment_form(invoice_id):
    invoice = models.Invoice.query.get(invoice_id)
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
        'total_price': invoice.total_price,
        'currency': invoice.currency
    }

    return render_template('payment_form.html', store_info=store_info, invoice_info=invoice_info)
