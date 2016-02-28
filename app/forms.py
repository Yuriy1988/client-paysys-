from wtforms import Form, StringField, PasswordField, IntegerField, SubmitField, validators


class UserPaymentForm(Form):
    # Card stuff:
    card_type = StringField('Card Type') # TODO: 'Make a checklist'
    card_number = StringField('Card Number', [validators.Length(min=16, max=16)])
    card_expire_month = StringField('Expire Month', [validators.Length(min=2, max=2)]) # TODO: 'Make a calendar picker'
    card_expire_year = StringField('Expire Year', [validators.Length(min=4, max=4)]) # TODO: 'Make a calendar picker'
    card_first_name = StringField('First Name', [validators.Length(min=1, max=30)])
    card_last_name = StringField('Last Name', [validators.Length(min=1, max=30)])

    # Payment stuff:
    payment_intent = StringField('Payment Intent', [validators.Length(min=1, max=30)]) # TODO: 'Make a checklist'
    payment_method = StringField('Payment Method', [validators.Length(min=1, max=30)]) # TODO: 'Make a checklist'
    amount_total = StringField('Amount', [validators.Length(min=1, max=100)])
    amount_currency = StringField('Currency', [validators.Length(min=3, max=3)]) # TODO: 'Make a checklist'
    payment_description = StringField('Payment Description', [validators.Length(min=0, max=300)])

    # etc:
    item = StringField('Item') # TODO: 'Male a checklist'.

    # Submit button:
    submit = SubmitField("Send")
