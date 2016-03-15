from marshmallow import fields, ValidationError
from marshmallow.validate import Length, OneOf, Range

from app.schemas import base
from app.models import enum


# Custom validators:
def must_be_more_than_0(data):
    if not data > 0:
        raise ValidationError('Quantity must be > 0.')

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


# Schemas:
class ItemSchema(base.BaseSchema):
    item_id = fields.Str(required=True)
    quantity = fields.Int(required=True, validate=must_be_more_than_0)
    unit_price = fields.Decimal(required=True, places=2)  # TODO: Check if places count works right.


class InvoiceSchema(base.BaseSchema):
    order_id = fields.Str(required=True)
    store_id = fields.Str(required=True)
    currency = fields.Str(required=True, validate=OneOf(enum.CURRENCY_ENUM), default='USD')
    items = fields.Nested(ItemSchema, validate=must_not_be_blank)
