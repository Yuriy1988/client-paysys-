from wtforms import Form, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


CARD_TYPE_CHOICES = [('visa','VISA'),('mastercard','MASTERCARD')]
PAYMENT_INTENT_CHOICES = [('sale','SALE')]
PAYMENT_METHOD_CHOICES = [('credit_card','CREDIT_CARD')]
ITEM_CHOICES = [('blue pen','Blue Pen'),('yellow jacket','Yellow Jacket'),('iphone 6s plus','iPhone 6s Plus')]
CURRENCY_CHOICES = [('USD','USD'),('EUR','EUR'),('GBP','GBP')]



class UserPaymentForm(Form):
    # Card stuff:
    card_type = SelectField('Card Type', validators=[DataRequired], choices=CARD_TYPE_CHOICES)
    card_number = StringField('Card Number', validators=[DataRequired, Length(min=16, max=16)], default='4417119669820331')
    card_expire_month = StringField('Expire Month', validators=[DataRequired, Length(min=2, max=2)], default='11') # TODO: 'Make a calendar picker'
    card_expire_year = StringField('Expire Year', validators=[DataRequired, Length(min=4, max=4)], default='2018') # TODO: 'Make a calendar picker'
    card_first_name = StringField('First Name', validators=[DataRequired, Length(min=1, max=30)], default='Joe')
    card_last_name = StringField('Last Name', validators=[DataRequired, Length(min=1, max=30)], default='Shopper')

    # Payment stuff:
    payment_intent = SelectField('Payment Intent', validators=[DataRequired, Length(min=1, max=30)], choices=PAYMENT_INTENT_CHOICES)
    payment_method = SelectField('Payment Method', validators=[DataRequired, Length(min=1, max=30)], choices=PAYMENT_METHOD_CHOICES)
    amount_total = StringField('Amount', validators=[DataRequired, Length(min=1, max=100)], default='6.70')
    amount_currency = SelectField('Currency', validators=[DataRequired, Length(min=3, max=3)], choices=CURRENCY_CHOICES)
    payment_description = StringField('Payment Description', validators=[Length(min=0, max=300)], default='')

    # etc:
    item = SelectField('Item', validators=[DataRequired], choices=ITEM_CHOICES) # TODO: 'Male a checklist'.

    # Submit button:
    submit = SubmitField("Send")
