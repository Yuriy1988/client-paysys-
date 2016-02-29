import json
import requests
from flask import render_template, request, redirect, flash
from wtforms import validators

from app import app
from app.forms import UserPaymentForm


class Shop:
    """
    Fake Shop model.
    """
    def __init__(self, id, name, logo):
        self.id = id
        self.name = name
        self. logo = logo

# DataBase:
shop1 = Shop("1", "Shop1", "pass_to_image1")
shop2 = Shop("2", "Shop2", "pass_to_image2")
shop3 = Shop("3", "Shop3", "pass_to_image3")
shops = [shop1, shop2, shop3]


@app.route('/')
def home():
    """
    Homepage with a shops list.
    """
    # TODO: Getting the list of all Shop objects.
    return render_template('home.html', shops=shops)


@app.route('/form/<shop_id>', methods=["GET", "POST"])
def user_payment_form(shop_id):
    """
    Showing the payment form.
    """
    # TODO: Add a csrf protection to form!
    # Faking the getting a Shop object by ID:
    for i in shops:
        if shop_id == i.id:
            shop = i

    form = UserPaymentForm()

    return render_template('user_payment_form.html', form=form, shop=shop)


@app.route('/form/<shop_id>/payment', methods=["GET", "POST"])
def user_payment_form_execute(shop_id):
    """
    Getting form POST values.
    Getting an auth PayPal token using client id and secret key.
    Adding user's card to storage and getting card id.
    Creating a payment using card id.
    """
    for i in shops:
        if shop_id == i.id:
            shop = i

    form = UserPaymentForm(request.form)

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
                               item=item,
                               shop=shop.name)
    else:
        err = form.errors
        return render_template('user_payment_form.html', form=form, shop=shop, err=err)