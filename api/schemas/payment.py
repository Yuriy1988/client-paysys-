import re
from marshmallow import fields, post_load, validates_schema, ValidationError
from marshmallow.validate import OneOf, Length, Email

from api.schemas import base
from api.models import enum

__author__ = 'Kostel Serhii'

# Visa : 13 or 16 digits, starting with 4.
# MasterCard : 16 digits, starting with 51 through 55.
# Card can be already masked.
_visa_master_regexp = re.compile(
    "^(4[0-9]{3}[0-9\*]{8}[0-9]{4}|4[0-9]{3}[0-9\*]{5}[0-9]{4}|5[1-5][0-9]{2}[0-9\*]{8}[0-9]{4})$")


class PaymentSchema(base.BaseSchema):

    id = fields.Str(dump_only=True)
    paysys_id = fields.Str(required=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM))
    payment_account = fields.Str(required=True, validate=Length(min=10, max=127))
    crypted_payment = fields.Str(required=True, validate=Length(min=1, max=4096))

    status = fields.Str()

    notify_by_email = fields.Email(allow_none=True)
    notify_by_phone = fields.Str(allow_none=True, validate=base.Phone())

    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    invoice_id = fields.Str(dump_only=True)

    @validates_schema
    def validate_payment_account(self, data):
        """
        Check payment account depending on the payment system.
        :param data: payment json
        """
        if data['paysys_id'] == 'VISA_MASTER':
            cleaned_pa = re.sub('[- ]', '', data['payment_account'])
            if not _visa_master_regexp.match(cleaned_pa):
                raise ValidationError('Wrong Visa/Master payment account.')

        elif data['paysys_id'] == 'PAY_PAL':
            Email(error='Wrong PayPal payment account.')(data['payment_account'])

    @post_load
    def mask_payment_account(self, data):
        """
        Mask Visa/Master card numbed as:
        16 dig: 4123 1234 5678 9870 -> 4123 **** **** 9870
        13 dig: 4123 12345 9870 -> 4123 ***** 9870
        :param data: payment data
        :return: payment data with masked payment account
        """
        if data['paysys_id'] == 'VISA_MASTER':
            cleaned_pa = re.sub('[- ]', '', data['payment_account'])
            pa_len = len(cleaned_pa)
            prefix, suffix = cleaned_pa[:4], cleaned_pa[-4:]
            center = '**** ****' if pa_len >= 16 else '*' * (pa_len - 8)
            data['payment_account'] = ' '.join((prefix, center, suffix))

        return data
