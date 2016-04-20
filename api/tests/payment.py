from flask import json

from api.tests import base
from api.models import Payment, Invoice

__author__ = 'Andrey Kupriy'


class TestPayment(base.BaseTestCase):

    # POST invoices/<invoice_id>/payments/visa_master

    def test_post_payment_valid_response(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post(
            '/invoices/{invoice_id}/payments'.format(invoice_id=invoice_body['id']),
            payment_request
        )

        self.assertEqual(payment_status, 202)
        # payment id generated:
        self.assertIn('id', payment_body)
        # status added:
        self.assertIn('status', payment_body)

    def test_post_payment_response_wrong_invoice_id(self):
        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/4k3k-kde3-ofkl-3345-sdada2-2a/payments/visa_master', payment_request)

        self.assertEqual(payment_status, 404)

    def test_payment_saved_to_db(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        invoice = Invoice.query.get(invoice_body['id'])
        payment = Payment.query.filter_by(invoice_id=invoice.id).one()

        self.assertIsNotNone(payment)
        self.assertIsNotNone(payment.id)
        self.assertEqual(payment.payment_account, "111111******1111")
        self.assertEqual(payment.status, "ACCEPTED")
        self.assertEqual(payment.notify_by_email, "email@email.com")
        self.assertEqual(payment.notify_by_phone, "111111111111")
        self.assertEqual(payment.invoice_id, invoice_body['id'])

    def test_payment_account_required(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        del payment_request['payment_account']
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['payment_account'], ['Missing data for required field.'])

    # cardholder_name validation

    def test_crypted_payment_required(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        del payment_request['crypted_payment']
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['crypted_payment'], ['Missing data for required field.'])

    # cvv validation

    def test_paysys_id_must_not_be_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_request['paysys_id'] = None
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['paysys_id'], ['Field may not be null.'])

    def test_paysys_id_must_be_enum(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_request['paysys_id'] = 'ddd'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['paysys_id'], ['Not a valid choice.'])

    def test_crypted_payment_not_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_request['crypted_payment'] = None
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['crypted_payment'], ['Field may not be null.'])

    # Change Payment status API

    def test_payment_change_status_response(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(updated_payment.status, status['status'])
        self.assertEqual(payment_change.status, '200 OK')

    def test_payment_change_status_upgrade_time(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()
        updated_time = payment.updated

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertNotEqual(updated_payment.updated, updated_time)

    def test_payment_change_status_no_request_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id=payment.id),
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(payment_change.status, '400 BAD REQUEST')

    def test_payment_change_status_empty_request_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        new_status = json.dumps("")
        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(payment_change.status, '400 BAD REQUEST')

    def test_payment_change_status_response_bad_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = {"s": "UPDATED"}
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '200 OK')
        self.assertNotEqual(updated_payment.status, "UPDATED")

    def test_payment_change_status_bad_payment_id(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id='97f65e39-e5cb-4b28-841d-8420f693bdbd'),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '404 NOT FOUND')

    def test_payment_change_status_bad_payment_id2(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id='lol'),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '404 NOT FOUND')

    def test_payment_change_status_bad_payment_id3(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        payment_request = self.get_payment_request()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments'.format(
            invoice_id=invoice_body['id']), payment_request)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}'.format(payment_id='nothing'),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '404 NOT FOUND')