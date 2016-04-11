from marshmallow import fields
from marshmallow.validate import OneOf, Range

from api.schemas import base
from api.models import enum


class ItemSchema(base.BaseSchema):
    store_item_id = fields.Str(required=True)
    quantity = fields.Int(required=True, validate=Range(min=1))
    unit_price = fields.Decimal(required=True, places=2)
    item_name = fields.Str(required=False, default=None)


class InvoiceSchema(base.BaseSchema):
    id = fields.Str(dump_only=True)
    payment_url = fields.Url(allow_none=True, default=None)
    order_id = fields.Str(required=True)
    store_id = fields.Str(required=True)
    currency = fields.Str(required=True, validate=OneOf(enum.CURRENCY_ENUM), default="USD")
    items = fields.Nested(ItemSchema, many=True, required=True, allow_none=False)

