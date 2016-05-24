from flask import json

from api.tests import base
from api.models import Payment, Invoice

__author__ = 'Andrey Kupriy'


class TestPayment(base.BaseTestCase):

    # POST invoices/<invoice_id>/payments/visa_master

    def test_post_payment_valid_response(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        self.assertEqual(payment_status, 202)
        # payment id generated:
        self.assertIn('id', payment_body)
        # status added:
        self.assertIn('status', payment_body)

    def test_post_payment_response_wrong_invoice_id(self):
        payment_request = self.get_payment()
        payment_status, payment_body = self.post(
            url='/invoices/4k3k-kde3-ofkl-3345-sdada2-2a/payments/visa_master',
            body=payment_request
        )

        self.assertEqual(payment_status, 404)

    def test_payment_saved_to_db(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        invoice = Invoice.query.get(invoice_body['id'])
        payment = Payment.query.filter_by(invoice_id=invoice.id).one()

        self.assertIsNotNone(payment)
        self.assertIsNotNone(payment.id)
        self.assertEqual(payment.payment_account, "4123 98** **** 0000")
        self.assertEqual(payment.status, "ACCEPTED")
        self.assertEqual(payment.notify_by_email, "email@email.com")
        self.assertEqual(payment.notify_by_phone, "380111234567")
        self.assertEqual(payment.invoice_id, invoice_body['id'])

    def test_payment_account_required(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        del payment_request['payment_account']
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['payment_account'], ['Missing data for required field.'])

    # cardholder_name validation

    def test_crypted_payment_required(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        del payment_request['crypted_payment']
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['crypted_payment'], ['Missing data for required field.'])

    # cvv validation

    def test_paysys_id_must_not_be_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_request['paysys_id'] = None
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['paysys_id'], ['Field may not be null.'])

    def test_paysys_id_must_be_enum(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_request['paysys_id'] = 'ddd'
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['paysys_id'], ['Not a valid choice.'])

    def test_crypted_payment_not_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_request['crypted_payment'] = None
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['crypted_payment'], ['Field may not be null.'])

    # Change Payment status API

    def test_payment_change_status_response(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        new_status = self.get_new_status()
        status, body = self.put('/payment/%s' % payment.id, body=new_status, token=self.get_system_token())
        self.assertEqual(status, 200)

        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()
        self.assertEqual(updated_payment.status, new_status['status'])

    def test_payment_change_status_upgrade_time(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()
        updated_time = payment.updated

        status, body = self.put('/payment/%s' % payment.id, body=self.get_new_status(), token=self.get_system_token())
        self.assertEqual(status, 200)

        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()
        self.assertNotEqual(updated_payment.updated, updated_time)

    def test_payment_change_status_empty_request_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status, body = self.put('/payment/%s' % payment.id, body='', token=self.get_system_token())
        self.assertEqual(status, 400)

    def test_payment_change_status_response_bad_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        payment_status, payment_body = self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status, body = self.put('/payment/%s' % payment.id, body={"s": "UPDATED"}, token=self.get_system_token())
        self.assertEqual(status, 200)

        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()
        self.assertNotEqual(updated_payment.status, "UPDATED")

    def test_payment_change_status_bad_payment_id(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment()
        self.post('/invoices/%s/payments' % invoice_body['id'], payment_request)

        for pay_id in ['97f65e39-e5cb-4b28-841d-8420f693bdbd', 'lol', 'nothing']:
            status, body = self.put(
                url='/payment/%s' % pay_id,
                body=self.get_new_status(),
                token=self.get_system_token()
            )
            self.assertEqual(status, 404)
