from api import db
from api.models import base, enum
from periphery.admin_api import send_email, send_sms


class Payment(base.BaseModel):

    __tablename__ = 'payment'

    id = db.Column(db.String, primary_key=True, default=base.uuid_id)
    paysys_id = db.Column(db.Enum(*enum.PAYMENT_SYSTEMS_ID_ENUM, name='enum_payment_systems'), nullable=False)
    payment_account = db.Column(db.String(127), nullable=False)

    status = db.Column(db.Enum(*enum.PAYMENT_STATUS_ENUM, name='enum_payment_status'), default='CREATED')

    notify_by_email = db.Column(db.String(255))
    notify_by_phone = db.Column(db.String(16))

    created = db.Column(db.DateTime(timezone=True), server_default=base.now_dt)
    updated = db.Column(db.DateTime(timezone=True), server_default=base.now_dt, onupdate=base.now_dt)

    invoice_id = db.Column(db.String, db.ForeignKey('invoice.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, paysys_id, payment_account, invoice_id, crypted_payment,
                 status='CREATED', notify_by_email=None, notify_by_phone=None):
        # create id to use it before commit (in transaction)
        self.id = base.uuid_id()

        self.paysys_id = paysys_id
        self.payment_account = payment_account

        self.status = status

        self.notify_by_email = notify_by_email
        self.notify_by_phone = notify_by_phone

        self.invoice_id = invoice_id

        self._crypted_payment = crypted_payment

    def __repr__(self):
        return '<Payment id: %r>' % self.id

    @property
    def crypted_payment(self):
        return self._crypted_payment


@base.on_model_event(Payment, 'after_insert')
@base.on_model_event(Payment, 'after_update')
def send_notifications(payment):
    """
    If something changed - send notification.
    :param payment: Payment model instance
    """
    if payment.notify_by_email:
        send_email(
            payment.notify_by_email,
            'XOPay transaction status',
            'Thank you for your payment! Transaction status is: {status}'.format(status=payment.status)
        )
    if payment.notify_by_phone:
        send_sms(
            payment.notify_by_phone,
            'XOPay transaction status is: {status}'.format(status=payment.status)
        )
