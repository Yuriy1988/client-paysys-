from app import db
import datetime


class Payment(db.Model):

    __tablename__ = 'payment'

    id = db.Column(db.String, nullable=True, unique=True, primary_key=True)
    card_number = db.Column(db.String(24), nullable=False)  # TODO: must be encrypted, digits only, len 12-24
    cardholder_name = db.Column(db.String, nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    expiry_date = db.Column(db.String, nullable=False)
    notify_by_email = db.Column(db.String(120))
    notify_by_phone = db.Column(db.String(120))
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id'))
    invoice = db.relationship('Invoice', backref='payment', lazy='dynamic')

    def __init__(self, id, card_number, cardholder_name, cvv, expiry_date, notify_by_email, notify_by_phone, invoice):
        self.id = id
        self.card_number = card_number
        self.cardholder_name = cardholder_name
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.notify_by_email = notify_by_email
        self.notify_by_phone = notify_by_phone
        self.invoice = invoice

    def __repr__(self):
        return '<Payment id: %r>' % self.id