from marshmallow import fields
from client.schemas import base
from marshmallow.validate import OneOf
from client.models import enum


class StatisticsArgsSchema(base.BaseSchema):
    limit = fields.Str(allow_none=True)
    from_date = fields.Date(allow_none=True)
    till_date = fields.Date(allow_none=True)
    payment_id = fields.Str(allow_none=True)
    transaction_id = fields.Str(allow_none=True)
    paysys_id = fields.Str(allow_none=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM))
    status = fields.Str(allow_none=True, validate=OneOf(enum.PAYMENT_STATUS_ENUM))
    currency = fields.Str(allow_none=True, validate=OneOf(enum.CURRENCY_ENUM))
