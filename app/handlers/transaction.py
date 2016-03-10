import json

import requests
from flask import render_template

from app import app, db
from app.models import Transaction

from config import helper_url, processing_url


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
        item_identifier=form_data['item_identifier'],
        store_identifier=form_data['store_identifier'],
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
    helper_json_response = requests.post(helper_url, data=json.dumps(helper_request))
    helper_response = json.loads(helper_json_response)

    processing_request = parse_processing_request(form_data, helper_response)
    processing_json_response = requests.post(processing_url, data=json.dumps(processing_request))
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
    transactions = Transaction.query.all()
    return render_template('home.html', transactions=transactions)
