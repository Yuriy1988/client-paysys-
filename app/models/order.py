from app import db
import datetime


class Order(db.Model):

    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    store_id = db.Column(db.String(127), nullable=False)
    item_id = db.Column(db.String(127))
    quantity = db.Column(db.Integer)
    amount_total = db.Column(db.String(300))
    amount_currency = db.Column(db.String(3), default='USD', nullable=False)
    transactions = db.relationship('Transaction', backref='transaction', lazy='dynamic')

    def __init__(self, store_id, item_id, quantity, amount_total, amount_currency):
        self.store_id = store_id
        self.item_id = item_id
        self.quantity = quantity
        self.amount_total = amount_total
        self.amount_currency = amount_currency

    def __repr__(self):
        return '<Order id: %r>' % self.id
