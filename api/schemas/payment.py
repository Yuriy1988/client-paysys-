from marshmallow import fields
from api.schemas import base, InvoiceSchema
from marshmallow.validate import OneOf, Length
from api.models import enum


class VisaMasterSchema(base.BaseSchema):
    card_number = fields.Str(required=True, validate=[Length(min=12, max=24), base.validate_digits_only])
    cardholder_name = fields.Str(required=True)
    cvv = fields.Str(required=True, validate=[Length(min=3, max=3), base.validate_digits_only])
    expiry_date = fields.Str(required=True, allow_none=False, validate=[Length(min=7, max=7),
                                                                        base.validate_card_expiry_date])
    notify_by_email = fields.Str()
    notify_by_phone = fields.Str()


class PaymentSchema(base.BaseSchema):
    id = fields.Str(dump_only=True)
    payment_account = fields.Str(required=True, validate=Length(min=12, max=24))
    status = fields.Str(required=True, validate=OneOf(enum.PAYMENT_STATUS_ENUM), default="ACCEPTED")
    notify_by_email = fields.Str()
    notify_by_phone = fields.Str()
    paysys_id = fields.Str(required=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM), default="USD")
    # invoice_id = fields.Nested(InvoiceSchema.id, required=True)
    invoice = fields.Nested(InvoiceSchema, required=True)
    created = fields.DateTime(required=True)
    updated = fields.DateTime()


class PaymentRequestSchema(base.BaseSchema):
    paysys_id = fields.Str(required=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM), default="USD")
    crypted_payment = fields.Str(required=True)
    payment_account = fields.Str(required=True)
    notify_by_email = fields.Str()
    notify_by_phone = fields.Str()


class PaymentResponseSchema(base.BaseSchema):
    id = fields.Str(required=True, validate=(Length(min=8, max=127)))
    status = fields.Str(required=True, validate=OneOf(enum.PAYMENT_STATUS_ENUM))