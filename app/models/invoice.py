from app import db
import datetime
from app.models import enum


class Item(db.Model):

    __tablename__ = 'item'

    item_id = db.Column(db.String, nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric, nullable=False)
    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id'))


class Invoice(db.Model):

    __tablename__ = 'invoice'

    id = db.Column(db.String, nullable=True, unique=True, primary_key=True)
    order_id = db.Column(db.String)
    store_id = db.Column(db.String, nullable=False)
    currency = db.Column(db.Enum(*enum.CURRENCY_ENUM, name='enum_currency'))
    items = db.relationship('Items', backref='invoice', lazy='dynamic')
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    payment = db.relationship('Payment', backref='invoice', lazy='dynamic')
    # payment_id = db.Column(db.String, db.ForeignKey('payment.id'))
    # transactions = db.relationship('Transaction', backref='transaction', lazy='dynamic')

    def __init__(self, id, order_id, store_id, currency, items):
        self.id = id
        self.order_id = order_id
        self.store_id = store_id
        self.currency = currency
        self.items = items

    def __repr__(self):
        return '<Invoice id: %r>' % self.id
