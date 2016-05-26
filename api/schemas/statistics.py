from marshmallow import fields
from api.schemas import base
from marshmallow.validate import OneOf, Length, Range
from api.models import enum


class StatisticsArgsSchema(base.BaseSchema):

    store_id = fields.Str(allow_none=True, validate=Length(equal=36))
    currency = fields.Str(allow_none=True, validate=OneOf(enum.CURRENCY_ENUM))
    from_total_price = fields.Decimal(allow_none=True)
    till_total_price = fields.Decimal(allow_none=True)

    paysys_id = fields.Str(allow_none=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM))
    payment_account = fields.Str(allow_none=True, validate=Length(max=127))
    status = fields.Str(allow_none=True, validate=OneOf(enum.PAYMENT_STATUS_ENUM))
    from_date = fields.Date(allow_none=True)
    till_date = fields.Date(allow_none=True)

    order_by = fields.Str(allow_none=True, missing='created', validate=Length(min=5, max=20))
    limit = fields.Int(allow_none=True, missing=10, validate=Range(min=1, max=30))
    offset = fields.Int(allow_none=True, missing=0, validate=Range(min=0))


class _StatisticsInvoiceSchema(base.BaseSchema):

    invoice_id = fields.Str(dump_only=True)
    store_id = fields.Str(dump_only=True)
    currency = fields.Str(dump_only=True)
    total_price = fields.Decimal(dump_only=True)


class StatisticsPaymentsSchema(base.BaseSchema):

    payment_id = fields.Str(dump_only=True)
    paysys_id = fields.Str(dump_only=True)
    payment_account = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    invoice = fields.Nested(_StatisticsInvoiceSchema, dump_only=True)

