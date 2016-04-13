from api.models import enum
from api.schemas.invoice import InvoiceSchema
from marshmallow import fields

from api.schemas import base
from marshmallow.validate import OneOf, Length, Range


class MerchantContractSchema(base.BaseSchema):
    id = fields.Integer()
    merchant_id = fields.String(required=True)
    commission_fixed = fields.Decimal(required=True)
    commission_pct = fields.Decimal(required=True, validate=Range(min=-100, max=100))
    currency = fields.String(required=True, validate=OneOf(enum.CURRENCY_ENUM), default="USD")


class PaySysContractSchema(base.BaseSchema):
    id = fields.Integer()
    contractor_name = fields.String(required=True)
    paysys_id = fields.String(required=True)
    commission_fixed = fields.Decimal(required=True)
    commission_pct = fields.Decimal(required=True, validate=Range(min=-100, max=100))
    currency = fields.String(required=True, validate=OneOf(enum.CURRENCY_ENUM), default="USD")
    payment_interface = fields.String(required=True)


class MerchantAccountSchema(base.BaseSchema):
    bank_name = fields.String(required=True)
    checking_account = fields.String(required=True)
    currency = fields.String(required=True, validate=OneOf(enum.CURRENCY_ENUM), default="USD")
    mfo = fields.String(required=True, validate=Length(equal=6))
    okpo = fields.String(required=True, validate=Length(min=8, max=10))


class PaymentRequisitesSchema(base.BaseSchema):
    crypted_payment = fields.String(required=True)


class PaymentSchema(base.BaseSchema):
    description = fields.String(required=True)
    invoice = fields.Nested(InvoiceSchema, required=True)
    amount_coins = fields.Integer(required=True, validate=Range(min=0))


class SourceSchema(base.BaseSchema):
    paysys_contract = fields.Nested(PaySysContractSchema, required=True)
    payment_requisites = fields.Nested(PaymentRequisitesSchema, required=True)


class DestinationSchema(base.BaseSchema):
    merchant_contract = fields.Nested(MerchantContractSchema, required=True)
    merchant_account = fields.Nested(MerchantAccountSchema, required=True)


class TransactionSchema(base.BaseSchema):
    id = fields.String(required=True)
    payment = fields.Nested(PaymentSchema, required=True)
    source = fields.Nested(SourceSchema, required=True)
    destination = fields.Nested(DestinationSchema, required=True)
