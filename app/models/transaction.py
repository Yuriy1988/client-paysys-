from app import db
import datetime
from app.models import enum


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String, db.ForeignKey('invoice.id'))
    transaction_id = db.Column(db.String(127), unique=True)  # TODO: Generate with UUID4
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(*enum.TRANSACTION_STATUS_ENUM, name='enum_transaction_status'))
    status_update = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Changes every status update
    amount_total = db.Column(db.Integer)
    amount_currency = db.Column(db.Enum(*enum.CURRENCY_ENUM, name='enum_currency'))
    payment_method = db.Column(db.Enum(*enum.PAYMENT_SYSTEMS_ID_ENUM, name='enum_payment_system_id'))
    store_id = db.Column(db.String(127), nullable=False)
    item_id = db.Column(db.String(127))

    # Source:
    payer_card_number = db.Column(db.String(16), nullable=False)  # TODO: must be encrypted
    payer_card_first_name = db.Column(db.String(33))
    payer_card_last_name = db.Column(db.String(33))

    # Destination:
    # TODO: Get info from HELPER?

    # Optional fields:
    payer_email = db.Column(db.String(50), nullable=True)
    payer_phone = db.Column(db.String(50), nullable=True)

    def __init__(self, order_id, transaction_id, amount_total, amount_currency, payment_method, store_id,
                 payer_card_number, payer_card_first_name, payer_card_last_name, payer_email,
                 payer_phone, status, item_id):
        self.order_id = order_id
        self.transaction_id = transaction_id
        self.status = status
        self.amount_total = amount_total
        self.amount_currency = amount_currency
        self.payment_method = payment_method
        self.store_id = store_id
        self.payer_card_number = payer_card_number
        self.payer_card_first_name = payer_card_first_name
        self.payer_card_last_name = payer_card_last_name
        self.payer_email = payer_email
        self.payer_phone = payer_phone
        self.item_id = item_id

    def __repr__(self):
        return '<Transaction id: %r>' % self.transaction_id
