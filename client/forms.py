from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import string


# Custom form validators:
def is_digit(form, field):
    if not field.data.isdigit():
        raise ValidationError('Card number must contain digits only.')


def latin_letters_only(form, field):
    all_the_letters = '{}{}- '.format(string.ascii_uppercase, string.ascii_lowercase)
    for i in field.data:
        if not i in all_the_letters:
            raise ValidationError('Card number must contain digits only.')


# Forms:
class VisaMasterPaymentForm(Form):
    card_number = StringField('Credit Card Number', validators=[DataRequired(), Length(min=12, max=24), is_digit])
    cardholder_name = StringField('Cardholder Name', validators=[DataRequired(), latin_letters_only])
    cvv = StringField('CVV', validators=[DataRequired(), is_digit, Length(min=3, max=3)])
    expiry_date = StringField('Expiry Date', validators=[DataRequired()])  # TODO: add a "mm/yyyy" format validator
    notify_by_email = StringField('Your Email', validators=[Email])
    notify_by_phone = StringField('Your Phone', validators=[is_digit])
