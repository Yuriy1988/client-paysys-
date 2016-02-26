from wtforms import Form, StringField, PasswordField, IntegerField, SubmitField, validators


class UserPaymentForm(Form):
    # PayPal user staff:
    email = StringField('Email Address')
    paypal_password = PasswordField('PayPal Password')

    # Transaction stuff:
    transaction_purpose = StringField('Transaction Purpose')
    amount = IntegerField('Amount')
    currency = StringField('Currncy')

    # Submit button:
    submit = SubmitField("Send")
