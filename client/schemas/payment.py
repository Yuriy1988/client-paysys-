from marshmallow import fields
from client.schemas import base, InvoiceSchema
from marshmallow.validate import Length


class VisaMasterSchema(base.BaseSchema):
    card_number = fields.Str(required=True, validate=[Length(min=12, max=24), base.validate_digits_only])
    cardholder_name = fields.Str(required=True)
    cvv = fields.Str(required=True, validate=[Length(min=3, max=3), base.validate_digits_only])
    expiry_date = fields.Str(required=True, allow_none=False, validate=[Length(min=7, max=7),
                                                                        base.validate_card_expiry_date])
    notify_by_email = fields.Str()
    notify_by_phone = fields.Str()


class PaymentSchema(base.BaseSchema):
    card_number = fields.Str(required=True, validate=Length(min=12, max=24))
    status = fields.Str(required=True, default="ACCEPTED")
    notify_by_email = fields.Str()
    notify_by_phone = fields.Str()
    invoice = fields.Nested(InvoiceSchema, required=True)


class PaymentResponceSchema(base.BaseSchema):
    id = fields.Str(required=True)
    status = fields.Str(required=True, default="ACCEPTED")

