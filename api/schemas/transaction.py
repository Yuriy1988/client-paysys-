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


TRANSACTION = {
    "id": "uuid",
    "payment": {
        "description": "string",
        "invoice": {
            "id": "uuid",
            "payment_url": "url",
            "order_id": "uuid",
            "store_id": "uuid",
            "currency": "enum",
            "items": [
                {
                    "store_item_id": "uuid",
                    "quantity": 0,
                    "unit_price": 0.0,
                    "item_name": "string"
                },
                ...
            ],
        },
        "amount_coins": 0,
    },
    "source": {
        "paysys_contract": {
            "id": 0,
            "contractor_name": "string",
            "paysys_id": "enum",
            "commission_fixed": 0.0,
            "commission_pct": 0.0,
            "currency": "enum"
        },
        "payment_requisites": {
            "crypted_payment": "crypted"
        }
    },
    "destination": {
        "merchant_contract": {
            "id": 0,
            "merchant_id": 0,
            "commission_fixed": 0.0,
            "commission_pct": 0.0,
            "currency": "enum"
        },
        "merchant_account": {
            "bank_name": "string",
            "checking_account": "",
            "currency": "enum",
            "mfo": "000000",
            "okpo": "00000000"
        }
    }
}
