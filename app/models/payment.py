import uuid
from copy import deepcopy

from app import db
import datetime
from app.models import base


class Payment(base.BaseModel):

    __tablename__ = 'payment'

    id = db.Column(db.String, nullable=True, unique=True, primary_key=True)
    card_number = db.Column(db.String(24), nullable=False)  # TODO: must be encrypted, digits only, len 12-24
    status = db.Column(db.String, default='ACCEPTED')  # TODO: may be will be transform into enum choices field.
    notify_by_email = db.Column(db.String(120))
    notify_by_phone = db.Column(db.String(120))
    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id'))
    invoice = db.relationship('Invoice')
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, card_number, status, notify_by_email, notify_by_phone, invoice):
        self.id = id
        self.card_number = card_number
        self.status = status
        self.notify_by_email = notify_by_email
        self.notify_by_phone = notify_by_phone
        self.invoice = invoice

    def __repr__(self):
        return '<Payment id: %r>' % self.id

    @classmethod
    def create(cls, data, add_to_db=True):
        data = deepcopy(data)

        data['id'] = str(uuid.uuid4())

        payment = super(Payment, cls).create(data)
        return payment