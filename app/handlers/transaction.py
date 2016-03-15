import json
import uuid

import requests
from flask import render_template, request, redirect, url_for

from app import app, db
from app.models import Transaction, Invoice

from config import HELPER_URL, PROCESSING_URL


def parse_helper_request(form_data):
    first_six = form_data['card_number'][0:6]
    dictionary = {
        'card_number': first_six,
        'store_id': form_data['store_id']
    }
    return dictionary


def parse_processing_request(form_data, helper_response):
    dictionary = {
        'payment_type': form_data['payment_method'],
        'source': {
            'card_number': form_data['card_number'],
            'cvv': form_data['card_cvv'],
            'expdate': '{month}/{year}'.format(month=form_data['card_expire_month'],
                                               year=form_data['card_expire_year[-2:]']),
            'cardholder_name': '{first_name} {last_name}'.format(first_name=form_data['card_first_name'],
                                                                 last_name=form_data['card_last_name'])
        },
        'destination': {
            'card_number': helper_response['card_number'],
            'cvv': helper_response['card_cvv'],
            'expdate': '{month}/{year}'.format(month=helper_response['card_expire_month'],
                                               year=helper_response['card_expire_year[-2:]']),
            'cardholder_name': '{first_name} {last_name}'.format(first_name=helper_response['card_first_name'],
                                                                 last_name=helper_response['card_last_name'])
        },
        'currency': form_data['amount_currency'],
        'amount_cent': form_data['amount_total'],
        'signature': form_data['payment_signature']
    }
    return dictionary


def save_transaction_to_db(form_data, processing_response):
    transaction = Transaction(
        payer_card_number=form_data['card_number'][0:6],
        payer_card_first_name=form_data['card_first_name'],
        payer_card_last_name=form_data['card_last_name'],
        item_id=form_data['item_id'],
        store_id=form_data['store_id'],
        amount_total=form_data['amount_total'],
        amount_currency=form_data['amount_currency'],
        payment_method=form_data['payment_method'],
        payer_email=form_data['payer_email'],
        payer_phone=form_data['payer_phone'],
        transaction_id=processing_response['transaction_id'],
        status=processing_response['status']
    )
    db.session.add(transaction)
    db.session.commit()
    return transaction.id


@app.route('/parse_transaction')
def parse_transaction(form_json_data):
    form_data = json.loads(form_json_data)

    helper_request = parse_helper_request(form_data)
    helper_json_response = requests.post(HELPER_URL, data=json.dumps(helper_request))
    helper_response = json.loads(helper_json_response)

    processing_request = parse_processing_request(form_data, helper_response)
    processing_json_response = requests.post(PROCESSING_URL, data=json.dumps(processing_request))
    processing_response = json.load(processing_json_response)

    transaction_id = save_transaction_to_db(form_data, processing_response)
    return render_template('thx.html', processing_response=processing_response, transaction_id=transaction_id)


@app.route('/get-transaction-status', methods=['GET', 'POST'])
def get_transaction_status(transaction_id):
    url = 'http://192.168.1.122:8888'
    data = {'PaymentID': transaction_id}  # TODO: Get transaction_id from processing.

    return requests.post(url, data=data)


@app.route('/')
def home():
    """
    Homepage with a shops list.
    """
    orders = Invoice.query.all()
    transactions = Transaction.query.all()
    return render_template('home.html', orders=orders, transactions=transactions)


@app.route('/credit_card_form', methods=['GET', 'POST'])
def credit_card_form():
    """
    Homepage with a shops list.
    """
    if request.method == 'POST':
        store_id = request.form['store_id']
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        amount_total = request.form['amount_total']
        amount_currency = request.form['amount_currency']

        order = Invoice(
            store_id=store_id,
            item_id=item_id,
            quantity=quantity,
            amount_total=amount_total,
            amount_currency=amount_currency
        )
        db.session.add(order)
        db.session.commit()
        return render_template('credit_card_form.html', order=order)

    else:
        return redirect(url_for('home'))


@app.route('/credit_card_form_execute/', methods=['GET', 'POST'])
def credit_card_form_execute():
    if request.method == 'POST':
        order_id = int(request.form['order_id'])
        store_id = request.form['store_id']
        item_id = request.form['item_id']
        amount_total = str(int(request.form['amount_total']) * 100)
        amount_currency = request.form['amount_currency']

        card_number = request.form['card_number']
        card_cvv = request.form['card_cvv']
        card_expire_month = request.form['expire_month']
        card_expire_year = request.form['expire_year']
        card_first_name = request.form['first_name']
        card_last_name = request.form['last_name']
        payment_method = 'PAY_PAL'
        payment_signature = 'eswdfewdf23fewr2'

        payer_email = request.form['payer_email']
        payer_phone = request.form['payer_phone']

        transaction_id = str(uuid.uuid4())
        status = 'NOT_FINAL'

        transaction = Transaction(
            order_id=order_id,
            transaction_id=transaction_id,
            status=status,
            amount_total=amount_total,
            amount_currency=amount_currency,
            payment_method=payment_method,
            store_id=store_id,
            payer_card_number=card_number,
            payer_card_first_name=card_first_name,
            payer_card_last_name=card_last_name,
            payer_email=payer_email,
            payer_phone=payer_phone,
            item_id=item_id
        )
        db.session.add(transaction)
        db.session.commit()

        return render_template('thank_you.html')

    else:
        err = "hi"
        return render_template('credit_card_form.html', err=err)
