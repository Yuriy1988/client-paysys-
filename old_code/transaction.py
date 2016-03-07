import json

import requests
from flask import render_template, request, jsonify

from app import app, db
from app.forms import PayPalPaymentForm, CreditCardForm
from app.models import Transaction


@app.route('/credit-card-form', methods=["GET", "POST"])
def credit_card_form():
    """
    Showing the Credit Card payment form.
    """
    # Getting the form:
    form = CreditCardForm()
    return render_template('credit_card_form.html', form=form)


#TODO: convert amount_total to cents

@app.route('/credit-card-form/execute', methods=["GET", "POST"])
def credit_card_form_execute():
    """
    Getting form POST values.
    Returning a JSON with payment details.
    """
    form = CreditCardForm(request.form)
    if request.method == 'POST' and form.validate():
        # Source:
        card_number = form.card_number.data
        card_cvv = form.card_cvv.data
        card_expire_month = form.card_expire_month.data
        card_expire_year = form.card_expire_year.data
        card_first_name = form.card_first_name.data
        card_last_name = form.card_last_name.data

        # Transaction staff:
        item_identifier = form.item_identifier.data
        store_identifier = form.store_identifier.data
        amount_total = form.amount_total.data  # TODO: Save in cents
        amount_currency = form.amount_currency.data
        payment_method = 'credit_card'

        # Destination:
        # TODO: Get destination method and info from HELPER!

        # Optional fields:
        payer_email = form.payer_email.data
        payer_phone = form.payer_phone.data

        # Secure processing stuff:
        payment_signature = "eswdfewdf23fewr2"

        dictionary = {
            'payment_type': payment_method,
            'source': {
                'card_number': card_number,
                'cvv': card_cvv,
                'expdate': '{month}/{year}'.format(month=card_expire_month, year=card_expire_year[-2:]),
                'cardholder_name': '{first_name} {last_name}'.format(first_name=card_first_name, last_name=card_last_name)
            },
            'destination': {
                '': ''
            },
            'currency': amount_currency,
            'amount_cent': amount_total,
            'signature': payment_signature
        }

        data = json.dumps(dictionary, sort_keys=False)

        url = 'http://192.168.1.122:8888'
        #r = requests.post(url, data=data)

        # Get from processing:
        transaction_id = 'sdfa'  # TODO: Get from Processing
        status = 'NOT_FINAL'  # TODO: Get from Processing

        trans = Transaction(
            payer_card_number=card_number,
            payer_card_first_name=card_first_name,
            payer_card_last_name=card_last_name,
            item_identifier=item_identifier,
            store_identifier=store_identifier,
            amount_total=amount_total,
            amount_currency=amount_currency,
            payment_method=payment_method,
            payer_email=payer_email,
            payer_phone=payer_phone,
            transaction_id=transaction_id,
            status=status
        )
        db.session.add(trans)
        db.session.commit()

        return render_template('thank_you.html',
                               #r=r,
                               data=data
                               )

    else:
        err = form.errors
        return render_template('credit_card_form.html', form=form, err=err)


@app.route('/paypal-form', methods=["GET", "POST"])
def paypal_form():
    """
    Showing the PayPal payment form.
    """
    # Getting the form:
    form = PayPalPaymentForm()
    return render_template('paypal_payment_form.html', form=form)


@app.route('/paypal-form/execute', methods=["GET", "POST"])
def paypal_form_execute():
    """
    Getting form POST values.
    Getting an auth PayPal token using client id and secret key.
    Adding user's card to storage and getting card id.
    Creating a payment using card id.
    """
    # Form POST processing:
    form = PayPalPaymentForm(request.form)
    if request.method == 'POST' and form.validate():

        # GETTING VALUES FROM THE FORM:
        # Card stuff:
        card_type = form.card_type.data
        card_number = form.card_number.data
        card_expire_month = form.card_expire_month.data
        card_expire_year = form.card_expire_year.data
        card_first_name = form.card_first_name.data
        card_last_name = form.card_last_name.data
        # Payment stuff:
        payment_intent = form.payment_intent.data
        payment_method = form.payment_method.data
        amount_total = form.amount_total.data
        amount_currency = form.amount_currency.data
        payment_description = form.payment_description.data
        # etc:
        item = form.item.data

        # GETTING PAYPAL ACCESS TOKEN:
        url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US'
        }
        username = 'AZrccVcbcXX1BpSsTTIioUdmvL2PLwznBTkwDFEcfORpz4i_BhE6FPwiQZRfa4RD0kepGAXF5oAWoY71'
        password = 'EEigCPS468DFBtGYmL3WdOscFxd6O7fxOObEI8ebX3uave3flC9iXzjymdNZUli0Y3HOKRSz8WLwIejf'
        auth = (username, password)
        data = {'grant_type': 'client_credentials'}
        # Request:
        r = requests.post(url, headers=headers, auth=auth, data=data)
        auth_token_status_code = 'Getting auth token status code: %s' % r.status_code
        # Getting access token and token type:
        r_dict = json.loads(r.text)
        access_token = r_dict['access_token']
        token_type = r_dict['token_type']

        # REGISTERING USER'S CARD:
        url = 'https://api.sandbox.paypal.com/v1/vault/credit-card'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': '{token_type} {access_token}'.format(token_type=token_type, access_token=access_token)
        }
        # Dumping card info to JSON:
        payer_id = 'user12345'
        data = json.dumps(
            {
                "payer_id":payer_id,
                 "type":card_type,
                 "number":card_number,
                 "expire_month":card_expire_month,
                 "expire_year":card_expire_year,
                 "first_name":card_first_name,
                 "last_name":card_last_name
            }
        )
        # Request:
        r = requests.post(url, headers=headers, data=data)
        register_card_status_code = 'Registering a card status code: %s' % r.status_code
        # Getting a Card ID and Payer ID:
        r_dict = json.loads(r.text)
        card_id = r_dict['id']
        payer_id = r_dict['payer_id']

        # USING A STORED CARD -- CREATING A PAYMENT:
        url = 'https://api.sandbox.paypal.com/v1/payments/payment'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': '{token_type} {access_token}'.format(token_type=token_type, access_token=access_token)
        }
        data = json.dumps(
            {
                'intent':payment_intent,
                'payer':{
                    'payment_method':payment_method,
                    'funding_instruments':[
                        {
                            'credit_card_token':{
                                'credit_card_id':card_id,
                                'payer_id':payer_id
                            }
                        }
                    ]
                },
                'transactions':[
                    {
                        'amount':{
                            'total':amount_total,
                            'currency':amount_currency
                        },
                        'description':payment_description
                    }
                ]
            }, sort_keys=True
        )
        # Request:
        r = requests.post(url, headers=headers, data=data)
        creating_payment_status_code = 'Creating a payment status code: %s' % r.status_code

        return render_template('thank_you.html',
                               auth_token_status_code=auth_token_status_code,
                               register_card_status_code=register_card_status_code,
                               creating_payment_status_code=creating_payment_status_code,
                               item=item
                               )
    else:
        err = form.errors
        return render_template('paypal_payment_form.html', form=form,err=err)


@app.route('/paypal-simple-form', methods=["GET", "POST"])
def paypal_simple_form():
    # Faking the getting a Shop object by ID:

    data = {
        'amount_total': '7.60',
        'amount_currency': 'USD',
        'business': "kin@kinskards.com",
        'cmd': '_cart',
        'add': '2',
        'item_name': 'Birthday - Cake and Candle'
    }
    return render_template('paypal_simple_payment_form.html', data=data)


@app.route('/bitcoin_form')
def bitcoin_form():
    pass