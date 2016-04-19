from decimal import Decimal
from marshmallow import fields
from marshmallow.validate import OneOf, Range, Length

from api.schemas import base
from api.models import enum

__author__ = 'Kostel Serhii'


class _ItemSchema(base.BaseSchema):

    store_item_id = fields.Str(required=True, validate=Length(min=1, max=512))
    quantity = fields.Int(required=True, validate=Range(min=1, max=1000))
    unit_price = fields.Decimal(required=True, validate=Range(min=Decimal('0.01'), max=Decimal(500000)))
    item_name = fields.Str(allow_none=True)


class InvoiceSchema(base.BaseSchema):

    id = fields.Str(dump_only=True)
    order_id = fields.Str(required=True, validate=Length(min=1, max=255))
    store_id = fields.Str(required=True, validate=Length(equal=36))
    currency = fields.Str(required=True, validate=OneOf(enum.CURRENCY_ENUM))
    items = fields.Nested(_ItemSchema, many=True, required=True, allow_none=False, validate=Length(min=1))

    payment_url = fields.Url(dump_only=True)
    total_price = fields.Decimal(dump_only=True)
