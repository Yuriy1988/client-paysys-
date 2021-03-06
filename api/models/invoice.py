from copy import deepcopy
from decimal import Decimal
from flask import url_for, current_app as app

from api import db
from api.models import enum, base


class Item(base.BaseModel):

    # NOTE: do NOT create/update Items manually only through Invoice.items.

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

    id = db.Column(db.String, primary_key=True, default=base.uuid_id)
    order_id = db.Column(db.String(255), nullable=False)
    store_id = db.Column(db.String(36), nullable=False)
    currency = db.Column(db.Enum(*enum.CURRENCY_ENUM, name='enum_currency'), nullable=False)
    total_price = db.Column(db.Numeric, nullable=False)

    created = db.Column(db.DateTime(timezone=True), server_default=base.now_dt)

    _items = db.relationship('Item', backref='invoice')
    payment = db.relationship('Payment', backref='invoice', uselist=False)

    def __init__(self, order_id, store_id, currency, items):
        self.order_id = order_id
        self.store_id = store_id
        self.currency = currency

        if len(items) < 1:
            raise ValueError('Blank list of items in the invoice')
        self._items = items

        total_price = self._calculate_total_price(items)
        if total_price < Decimal('0.01'):
            raise ValueError('Total price can not be less than 0.01')
        self.total_price = total_price

    def __repr__(self):
        return '<Invoice id: %r>' % self.id

    @property
    def payment_url(self):
        return app.config['SERVER_URL'] + url_for('pages.get_payment_form', invoice_id=self.id)

    @property
    def items(self):
        # NOTE: do NOT change items after Invoice creation, because
        # total_price calculated from them.
        return self._items

    @classmethod
    def create(cls, data, add_to_db=True):
        data = deepcopy(data)

        items_data = data.pop('items', [])
        data['items'] = [Item.create(it) for it in items_data]

        invoice = super(Invoice, cls).create(data)
        return invoice

    @staticmethod
    def _calculate_total_price(items):
        return sum(Decimal(it.unit_price) * Decimal(it.quantity) for it in items)
