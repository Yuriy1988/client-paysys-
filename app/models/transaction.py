from app import db
import datetime
from . import enum


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(127))  # Get from Processing
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(*enum.TRANSACTION_STATUS_ENUM), default='NOT_FINAL', nullable=False)
    status_update = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # Changes every status update
    amount_total = db.Column(db.Integer)
    amount_currency = db.Column(db.Enum(*enum.CURRENCY_ENUM), default='USD', nullable=False)
    payment_method = db.Column(db.Enum(*enum.PAYMENT_METHODS_ENUM), default='CREDIT_CARD', nullable=False)
    store_identifier = db.Column(db.String(127), nullable=False, unique=True)
    item_identifier = db.Column(db.String(127))

    # Source:
    payer_card_number = db.Column(db.String(16), nullable=False) # TODO: must be encrypted
    # payer_card_expiration_date = db.Column(db.String(5), nullable=False) # TODO: may be we need to use a DateField or two IntegerFields (one for month and one for year)
    # payer_card_cvv = db.Column(db.String(3), nullable=False)
    payper_first_name = db.Column(db.String(33), nullable=True)
    payper_last_name = db.Column(db.String(33), nullable=True)

    # Destination:
    # TODO: how I'll get info from HELPER?

    # Optional fields:
    payer_email = db.Column(db.String(50), nullable=True)
    payer_phone = db.Column(db.Integer, nullable=True)

    def __init__(self, transaction_id, creation_date, status_update, amount_total, amount_currency,
                 payment_method, store_identifier, payer_card_number=None, payer_first_name=None, payer_last_name=None,
                 payer_email=None, payer_phone=None, status=None):
        self.transaction_id = transaction_id
        self.creation_date = creation_date
        self.status = status
        self.status_update = status_update
        self.amount_total = amount_total
        self.amount_currency = amount_currency
        self.payment_method = payment_method
        self.store_identifier = store_identifier
        self.payer_card_number = payer_card_number
        self.payer_first_name = payer_first_name
        self.payer_last_name = payer_last_name
        self.payer_email = payer_email
        self.payer_phone = payer_phone

    def __repr__(self):
        return '<Transaction id: %r>' % self.transaction_id