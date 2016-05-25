from api import db, services
from api.models import base, enum


class Payment(base.BaseModel):

    __tablename__ = 'payment'

    id = db.Column(db.String, primary_key=True)
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
        # use the same id as invoice_id
        self.id = invoice_id

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
        message = ''

        if payment.status == 'SUCCESS':
            message = 'Thank you for your payment!\nTransaction [%s] status is success!' % payment.id

        if payment.status == 'REJECTED':
            message = 'Sorry, but your transaction [%s] is rejected.\nTry agen later.' % payment.id

        if message:
            services.send_email(payment.notify_by_email, subject='XOPay transaction status', message=message)

    if payment.notify_by_phone:
        if payment.status in ['SUCCESS', 'REJECTED']:
            services.send_sms(payment.notify_by_phone, 'XOPay transaction status is %s' % payment.status)
