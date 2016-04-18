from marshmallow import fields
from marshmallow.validate import OneOf, Length

from api.schemas import base
from api.models import enum

__author__ = 'Kostel Serhii'


class PaymentSchema(base.BaseSchema):

    id = fields.Str(dump_only=True)
    paysys_id = fields.Str(required=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM))
    payment_account = fields.Str(required=True, validate=Length(min=10, max=127))
    crypted_payment = fields.Str(required=True, validate=Length(min=1, max=4096))

    status = fields.Str(dump_only=True)

    notify_by_email = fields.Email(allow_none=True)
    notify_by_phone = fields.Str(allow_none=True, validate=base.Phone())

    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    invoice_id = fields.Str(dump_only=True)
