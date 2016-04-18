import pytz
import uuid
from datetime import datetime
from decimal import Decimal
from flask import url_for

from api import db
from api.models import enum, base
from copy import deepcopy


class Item(base.BaseModel):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    store_item_id = db.Column(db.String(512), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric, nullable=False)
    item_name = db.Column(db.String(512))

    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, store_item_id, quantity, unit_price, item_name=None):
        self.store_item_id = store_item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.item_name = item_name

    def __repr__(self):
        return '<Item %r>' % self.id


class Invoice(base.BaseModel):

    __tablename__ = 'invoice'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(255), nullable=False)
    store_id = db.Column(db.String(36), nullable=False)
    currency = db.Column(db.Enum(*enum.CURRENCY_ENUM, name='enum_currency'), nullable=False)

    items = db.relationship('Item', backref='invoice')
    payment = db.relationship('Payment', backref='invoice', uselist=False)

    created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(tz=pytz.utc))

    def __init__(self, order_id, store_id, currency, items):
        self.order_id = order_id
        self.store_id = store_id
        self.currency = currency
        if len(items) < 1:
            raise ValueError('Blank list of items in the invoice')
        self.items = items

    def __repr__(self):
        return '<Invoice id: %r>' % self.id

    @property
    def payment_url(self):
        return url_for('get_payment_form', invoice_id=self.id, _external=True)

    @property
    def amount(self):
        items_list = Item.query.filter_by(invoice_id=self.id).all()
        amount = 0
        for item in items_list:
            amount += Decimal(item.unit_price) * int(item.quantity)
        return round(amount, 2)

    @classmethod
    def create(cls, data, add_to_db=True):
        data = deepcopy(data)

        items_data = data.pop('items', [])
        data['items'] = [Item.create(it) for it in items_data]

        invoice = super(Invoice, cls).create(data)
        return invoice