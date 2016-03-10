import json
import requests
from flask import render_template, request
from app import app, db


#Fake items:
class Item:
    def __init__(self, id, logo, name, description, price):
        self.id = id
        self.logo = logo
        self.name = name
        self.description = description
        self.price = price

item1 = Item('1', 'pro.jpg', 'Apple Macbook Pro 15"', '15,4" • IPS • 2560x1600 • Intel Core i5-5257U • 2.7 - 3.1 ГГц • ОЗУ: \
8 ГБ • Intel Iris Graphics 6100 • SSD: 256 ГБ • 1,58 кг • ОС: OS X Yosemite', '1999')
item2 = Item('2', 'air.jpeg', 'Apple Macbook Air 13"', '13,3" • TN+film • 1400x900 • Intel Core i5-5250U • 1.6 - 2.7 ГГц • \
ОЗУ: 4 ГБ • Intel HD Graphics 6000 • SSD: 128 ГБ • 1,35 кг • ОС: OS X Yosemite', '899')
item3 = Item('3', 'mac.jpg', 'Apple Macbook 12"', '12" • IPS • 2304x1440 • Intel Core M-5Y31 • 1,1 ГГц • ОЗУ: 8 ГБ • Intel \
HD Graphics 5300 • SSD: 256 ГБ • 0,92 кг • ОС: OS X Yosemite', '1599')
items = [item1, item2, item3]

store_identifier = 'storeid2'
admin_url = 'http://192.168.1.105:7128/api/admin/dev/info/stores/'
processing_url = 'http://192.168.1.105:8888'


@app.route('/')
def home():
    """
    Homepage with a shops list.
    """
    return render_template('home.html', items=items)


@app.route('/credit-card-form/<item_id>', methods=["GET", "POST"])
def credit_card_form(item_id):
    """
    Showing the Credit Card payment form.
    """
    item = [i for i in items if i.id == item_id]
    item = item[0]

    # Getting store name:
    url = '{admin_url}{store_identifier}'.format(admin_url=admin_url, store_identifier=store_identifier)
    admin_json_shop_response = requests.get(url)
    admin_shop_response = json.loads(admin_json_shop_response.text)
    store_name = admin_shop_response['store_name']

    return render_template('credit_card_form.html', item=item, store_name=store_name)


@app.route('/credit-card-form/execute', methods=["GET", "POST"])
def credit_card_form_execute():
    """
    Getting form POST values.
    Returning a JSON with payment details.
    """
    if request.method == 'POST':

        # Source:
        card_number = request.form['card_number']
        print('!!!!!' + card_number)
        card_cvv = request.form['cvv']
        card_expire_month = request.form['expire_month']
        card_expire_year = request.form['expire_year']
        card_first_name = request.form['first_name']
        card_last_name = request.form['last_name']

        amount_total = str(int(request.form['amount']) * 100)  # TODO: Save in cents
        amount_currency = request.form['currency']
        payment_method = 'credit_card'
        payment_signature = 'eswdfewdf23fewr2'

        # Destination:
        url = '{admin_url}{store_identifier}/merchant_account'.format(admin_url=admin_url, store_identifier=store_identifier)
        admin_json_destination_response = requests.get(url)
        admin_destination_response = json.loads(admin_json_destination_response.text)


        dictionary = {
            'payment_type': payment_method,
            'source': {
                'card_number': card_number,
                'cvv': card_cvv,
                'expdate': '{month}/{year}'.format(month=card_expire_month, year=card_expire_year[-2:]),
                'cardholder_name': '{first_name} {last_name}'.format(first_name=card_first_name,
                                                                     last_name=card_last_name)
            },
            'destination': admin_destination_response,
            'currency': amount_currency,
            'amount_cent': amount_total,
            'signature': payment_signature
        }

        data = json.dumps(dictionary, sort_keys=False)

        r_json = requests.post(processing_url, data=data)

        r = json.loads(r_json.text)
        transaction_id = r['transaction_id']

        return render_template('thank_you.html',
                               transaction_id=transaction_id,
                               )

    else:
        err = "hi"
        return render_template('credit_card_form.html', err=err)


@app.route('/get-transaction-status', methods=['GET', 'POST'])
def get_transaction_status(transaction_id):
    url = url = 'http://192.168.1.122:8888'
    data = {'PaymentID': transaction_id}  # TODO: Get transaction_id from processing.

    return requests.post(url, data=data)
