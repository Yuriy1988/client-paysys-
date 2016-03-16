from marshmallow import fields
from app.schemas import base, InvoiceSchema


class VisaMasterSchema(base.BaseSchema):
    id = fields.Str(required=False, default=None)
    card_number = fields.Str(required=True)
    cardholder_name = fields.Str(required=True)
    cvv = fields.Str(required=True)
    expiry_date = fields.Str(required=True)
    notify_by_email = fields.Str()
    notify_by_phone = fields.Str()
    # invoice = fields.Nested(InvoiceSchema, required=True)


class PaymentResponceSchema(base.BaseSchema):
    id = fields.Str(required=True)
    status = fields.Str(required=True, default="ACCEPTED")
