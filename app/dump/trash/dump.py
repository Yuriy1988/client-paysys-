from app import app
from flask import render_template, request
from wtforms import Form, StringField, PasswordField, IntegerField, validators


@app.route('/simple', methods=["GET", "POST"])
def paypal_simple_form():
    form = PayPalSimplePaymentForm()
    return render_template('paypal_simple_form.html', form=form)


@app.route('/form_action', methods=["POST"])
def form_action():
    cmd = request.form['cmd']
    seller_email = request.form['business']
    item_name = request.form['item_name']
    item_number = request.form['item_number']
    amount = request.form['amount']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address1 = request.form['address1']
    address2 = request.form['address2']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    night_phone_a = request.form['night_phone_a']
    night_phone_b = request.form['night_phone_b']
    night_phone_c = request.form['night_phone_c']
    payer_email = request.form['email']

    dictionary = {
        'cmd': cmd,
        'seller_email': seller_email,
        'item_name': item_name,
        'item_number': item_number,
        'amount': amount,
        'first_name': first_name,
        'last_name': last_name,
        'address1': address1,
        'address2': address2,
        'city': city,
        'state': state,
        'zip': zip,
        'night_phone_a': night_phone_a,
        'night_phone_b': night_phone_b,
        'night_phone_c': night_phone_c,
        'payer_email': payer_email
    }
    return dictionary['payer_email']


@app.route('/simple_form_action', methods=["POST"])
def simple_form_action():
    email = request.form['email']
    paypal_password = request.form['paypal_password']
    return "{}, {}".format(email, paypal_password)



class PayPalSimplePaymentForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    paypal_password = PasswordField('PayPal Password')


class PayPalPaymentForm(Form):
    cmd = StringField('cmd', [validators.Length(min=1, max=200)])
    seller_email = StringField('seller_email', [validators.Length(min=6, max=35)])
    item_name = StringField('item_name', [validators.Length(min=1, max=200)])
    item_number = StringField('item_number', [validators.Length(min=1, max=200)])
    amount = IntegerField('amount', [validators.NumberRange(min=0, max=9999999999)])
    first_name = StringField('first_name', [validators.Length(min=1, max=100)])
    last_name = StringField('last_name', [validators.Length(min=1, max=100)])
    address1 = StringField('address1', [validators.Length(min=1, max=200)])
    address2 = StringField('address2', [validators.Length(min=1, max=200)])
    city = StringField('city', [validators.Length(min=1, max=35)])
    state = StringField('state', [validators.Length(min=1, max=35)])
    zip = StringField('zip', [validators.Length(min=2, max=35)])
    night_phone_a = StringField('night_phone_a', [validators.Length(min=1, max=35)])
    night_phone_b = StringField('night_phone_b', [validators.Length(min=1, max=35)])
    night_phone_c = StringField('night_phone_c', [validators.Length(min=1, max=35)])
    payer_email = StringField('payer_email', [validators.Length(min=6, max=35)])