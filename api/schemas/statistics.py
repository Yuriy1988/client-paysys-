from marshmallow import fields, validates_schema
from marshmallow.validate import OneOf, Length, Range

from api.schemas import base
from api.models import enum
from api.errors import ValidationError


class StatisticsArgsSchema(base.BaseSchema):

    store_id = fields.Str(allow_none=True, validate=Length(equal=36))
    currency = fields.Str(allow_none=True, validate=OneOf(enum.CURRENCY_ENUM))
    from_total_price = fields.Decimal(allow_none=True, places=2)
    till_total_price = fields.Decimal(allow_none=True, places=2)

    paysys_id = fields.Str(allow_none=True, validate=OneOf(enum.PAYMENT_SYSTEMS_ID_ENUM))
    payment_account = fields.Str(allow_none=True, validate=Length(max=127))
    status = fields.Str(allow_none=True, validate=OneOf(enum.PAYMENT_STATUS_ENUM))
    from_date = fields.Date(allow_none=True)
    till_date = fields.Date(allow_none=True)

    order_by = fields.Str(allow_none=True, missing='created', validate=Length(min=5, max=20))
    limit = fields.Int(allow_none=True, missing=10, validate=Range(min=1, max=30))
    offset = fields.Int(allow_none=True, missing=0, validate=Range(min=0))

    @validates_schema
    def validate_date(self, data):
        """Check date range: from < till.
        :param data: statistics args json
        """
        if not data:
            return

        from_date, till_date = data.get('from_date'), data.get('till_date')
        if from_date and till_date:
            if from_date > till_date:
                raise ValidationError('Till date must be grater than From date.')

    @validates_schema
    def validate_price(self, data):
        """Check price range: from < till.
        :param data: statistics args json
        """
        if not data:
            return

        from_total_price, till_total_price = data.get('from_total_price'), data.get('till_total_price')
        if from_total_price and till_total_price:
            if from_total_price > till_total_price:
                raise ValidationError('Till price must be grater than From price.')


class _StatisticsInvoiceSchema(base.BaseSchema):

    invoice_id = fields.Str(dump_only=True)
    store_id = fields.Str(dump_only=True)
    currency = fields.Str(dump_only=True)
    total_price = fields.Decimal(dump_only=True, places=2)


class StatisticsPaymentsSchema(base.BaseSchema):

    payment_id = fields.Str(dump_only=True)
    paysys_id = fields.Str(dump_only=True)
    payment_account = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    invoice = fields.Nested(_StatisticsInvoiceSchema, dump_only=True)

