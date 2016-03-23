import uuid

from client import db
import datetime
from client.models import enum, base
from copy import deepcopy


class Item(base.BaseModel):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    store_item_id = db.Column(db.String, nullable=False, default='default_store_item_id')
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric, nullable=False)
    item_name = db.Column(db.String)
    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id'))


class Invoice(base.BaseModel):

    __tablename__ = 'invoice'

    id = db.Column(db.String, nullable=True, unique=True, primary_key=True)
    payment_url = db.Column(db.String(255))
    order_id = db.Column(db.String)
    store_id = db.Column(db.String, nullable=False)
    currency = db.Column(db.Enum(*enum.CURRENCY_ENUM, name='enum_currency'))
    items = db.relationship('Item', backref='invoice', lazy='dynamic')
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    payment = db.relationship('Payment', lazy='dynamic')
    # transactions = db.relationship('Transaction', backref='transaction', lazy='dynamic')

    def __init__(self, id, order_id, store_id, currency, items):
        self.id = id
        self.order_id = order_id
        self.store_id = store_id
        self.currency = currency
        self.items = items

    def __repr__(self):
        return '<Invoice id: %r>' % self.id

    @classmethod
    def create(cls, data, add_to_db=True):
        data = deepcopy(data)

        # Generating a unique Invoice id:
        data['id'] = str(uuid.uuid4())

        items_data = data.pop('items', {})

        items_list = []
        for item in items_data:
            item = Item.create(item)
            db.session.commit()
            items_list.append(item)

        data['items'] = items_list

        invoice = super(Invoice, cls).create(data)
        return invoice
