import uuid
from copy import deepcopy

from api import db
import datetime
from api.models import base, enum


class Payment(base.BaseModel):

    __tablename__ = 'payment'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payment_account = db.Column(db.String(24))
    status = db.Column(db.Enum(*enum.PAYMENT_STATUS_ENUM, name='enum_payment_status'), default='ACCEPTED')
    notify_by_email = db.Column(db.String(120))
    notify_by_phone = db.Column(db.String(120))
    paysys_id = db.Column(db.Enum(*enum.PAYMENT_SYSTEMS_ID_ENUM, name='enum_payment_systems'), default='VISA_MASTER')
    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id'))
    invoice = db.relationship('Invoice')
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, payment_account, status, notify_by_email, notify_by_phone, paysys_id, invoice_id):
        self.payment_account = payment_account
        self.status = status
        self.notify_by_email = notify_by_email
        self.notify_by_phone = notify_by_phone
        self.paysys_id = paysys_id
        self.invoice_id = invoice_id

    def __repr__(self):
        return '<Payment id: %r>' % self.id

    @classmethod
    def create(cls, data, add_to_db=True):
        data = deepcopy(data)

        payment = super(Payment, cls).create(data)
        return payment