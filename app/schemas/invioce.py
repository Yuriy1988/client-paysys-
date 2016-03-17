from marshmallow import fields
from marshmallow.validate import OneOf, Range

from app.schemas import base
from app.models import enum


class ItemSchema(base.BaseSchema):
    item_id = fields.Str(required=True)
    quantity = fields.Int(required=True, validate=Range(min=1))
    unit_price = fields.Decimal(required=True, places=2)  # TODO: Check if places count works right.
    item_name = fields.Str(required=False, default=None)


class InvoiceSchema(base.BaseSchema):
    id = fields.Str(required=False, default=None)
    order_id = fields.Str(required=True)
    store_id = fields.Str(required=True)
    currency = fields.Str(required=True, validate=OneOf(enum.CURRENCY_ENUM), default='USD')
    items = fields.Nested(ItemSchema, many=True, required=True)

