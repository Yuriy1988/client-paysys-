from wtforms import Form, StringField, SubmitField, SelectField, HiddenField, validators


CARD_TYPE_CHOICES = [('visa', 'VISA'), ('mastercard', 'MASTERCARD')]
PAYMENT_INTENT_CHOICES = [('sale', 'SALE')]
PAYMENT_METHOD_CHOICES = [('credit_card', 'CREDIT_CARD')]
ITEM_CHOICES = [('blue pen', 'Blue Pen'), ('yellow jacket', 'Yellow Jacket'), ('iphone 6s plus', 'iPhone 6s Plus')]
CURRENCY_CHOICES = [('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')]


class PayPalPaymentForm(Form):
    """
    Form for paying via PayPal.
    """
    # Card stuff:
    card_type = SelectField(
        'Card Type',
        [validators.DataRequired(message='Sorry, this is a required field.')],
        choices=CARD_TYPE_CHOICES
    )
    card_number = StringField(
        'Card Number',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=16, max=16, message='Too long or too short')],
        default='4417119669820331'
    )
    card_expire_month = StringField(
        'Expire Month',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=2, max=2)],
        default='11'
    )  # TODO: 'Make a calendar picker'
    card_expire_year = StringField(
        'Expire Year',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=4, max=4)],
        default='2018'
    )  # TODO: 'Make a calendar picker'
    card_first_name = StringField(
        'First Name',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        default='Joe'
    )
    card_last_name = StringField(
        'Last Name',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        default='Shopper'
    )

    # Payment stuff:
    payment_intent = SelectField(
        'Payment Intent',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        choices=PAYMENT_INTENT_CHOICES
    )
    payment_method = SelectField(
        'Payment Method',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        choices=PAYMENT_METHOD_CHOICES
    )
    amount_total = StringField(
        'Amount',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=100)],
        default='6.70'
    )
    amount_currency = SelectField(
        'Currency',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=3, max=3)],
        choices=CURRENCY_CHOICES
    )
    payment_description = StringField(
        'Payment Description',
        [validators.Length(min=0, max=300)]
    )

    # etc:
    item = SelectField(
        'Item',
        [validators.DataRequired(message='Sorry, this is a required field.')],
        choices=ITEM_CHOICES
    )


class CreditCardPaymentForm(Form):
    """
    Form for paying via Credit Card.
    """
    # Card stuff:
    card_type = SelectField(
        'Card Type',
        [validators.DataRequired(message='Sorry, this is a required field.')],
        choices=CARD_TYPE_CHOICES
    )
    card_number = StringField(
        'Card Number',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=16, max=16, message='Too long or too short')],
        default='4417119669820331'
    )
    card_cvv = StringField(
        'CVV',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=3, max=3, message='Too long or too short')],
        default='987'
    )
    card_expire_month = StringField(
        'Expire Month',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=2, max=2)],
        default='11'
    )  # TODO: 'Make a calendar picker'
    card_expire_year = StringField(
        'Expire Year',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=4, max=4)],
        default='2018'
    )  # TODO: 'Make a calendar picker'
    card_first_name = StringField(
        'First Name',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        default='Joe'
    )
    card_last_name = StringField(
        'Last Name',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        default='Shopper'
    )

    # Payment stuff:
    payment_intent = HiddenField(
        'Payment Intent',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        default='sale'
        #choices=PAYMENT_INTENT_CHOICES
    )
    payment_method = HiddenField(
        'Payment Method',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=30)],
        default='credit_card'
        #choices=PAYMENT_METHOD_CHOICES
    )
    amount_total = HiddenField(
        'Amount',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=1, max=100)],
        default='6.70'
    )
    amount_currency = HiddenField(
        'Currency',
        [validators.DataRequired(message='Sorry, this is a required field.'),
         validators.Length(min=3, max=3)],
        default='USD'
        #choices=CURRENCY_CHOICES
    )
    payment_description = StringField(
        'Payment Description',
        [validators.Length(min=0, max=300)],
        default=''
    )

    # etc:
    item = HiddenField(
        'Item',
        [validators.DataRequired(message='Sorry, this is a required field.')],
        default='item'
        #choices=ITEM_CHOICES
    )
