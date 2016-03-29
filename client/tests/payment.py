import json

from client.tests import base
from client.models import Payment, Invoice

__author__ = 'Andrey Kupriy'


class TestPayment(base.BaseTestCase):

    # POST invoices/<invoice_id>/payments/visa_master

    def test_post_payment_valid_response(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 202)
        # payment id generated:
        self.assertIn('id', payment_body)
        # status added:
        self.assertIn('status', payment_body)

    def test_post_payment_response_wrong_invoice_id(self):
        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/4k3k-kde3-ofkl-3345-sdada2-2a/payments/visa_master', card_info)

        self.assertEqual(payment_status, 404)

    def test_payment_saved_to_db(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        invoice = Invoice.query.get(invoice_body['id'])
        payment = Payment.query.filter_by(invoice_id=invoice.id).one()

        self.assertIsNotNone(payment)
        self.assertIsNotNone(payment.id)
        self.assertEqual(payment.card_number, "111111******1111")
        self.assertEqual(payment.status, "ACCEPTED")
        self.assertEqual(payment.notify_by_email, "email@email.com")
        self.assertEqual(payment.notify_by_phone, "111111111111")
        self.assertEqual(payment.invoice_id, invoice_body['id'])

    # card_number validation

    def test_card_number_must_have_digits_only(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['card_number'] = '11111dddddd11111111'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['card_number'], ['Card number must contain digits only'])

    def test_card_number_must_have_12_24_length(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['card_number'] = '1'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['card_number'], ['Length must be between 12 and 24.'])

    def test_card_number_must_not_be_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['card_number'] = None
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['card_number'], ['Field may not be null.'])

    # cardholder_name validation

    def test_cardholder_name_must_not_be_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['cardholder_name'] = None
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['cardholder_name'], ['Field may not be null.'])

    # cvv validation

    def test_cvv_must_not_be_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['cvv'] = None
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['cvv'], ['Field may not be null.'])

    def test_cvv_must_have_digits_only(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['cvv'] = 'ddd'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['cvv'], ['Card number must contain digits only'])

    def test_cvv_must_have_3_length(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['cvv'] = '1'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['cvv'], ['Length must be between 3 and 3.'])

    # expiry_date validation

    def test_card_expiry_date_must_not_be_none(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['expiry_date'] = None
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['expiry_date'], ['Field may not be null.'])

    def test_card_expiry_date_format_validation(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['expiry_date'] = 'ddddddd'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['expiry_date'],
                         ['Wrong card expiry date format. Required format: "11/1111"'])

    def test_cvv_must_have_7_length(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        card_info['expiry_date'] = '1'
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        self.assertEqual(payment_status, 400)
        self.assertEqual(payment_body['error']['errors']['expiry_date'],
                         ['Length must be between 7 and 7.',
                          'Wrong card expiry date format. Required format: "11/1111"'])

    # Change Payment status API

    def test_payment_change_status_responce(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(updated_payment.status, status['status'])
        self.assertEqual(payment_change.status, '200 OK')

    def test_payment_change_status_upgrade_time(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()
        updated_time = payment.updated

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertNotEqual(updated_payment.updated, updated_time)

    def test_payment_change_status_no_request_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id=payment.id),
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(payment_change.status, '400 BAD REQUEST')

    def test_payment_change_status_empty_request_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        new_status = json.dumps("")
        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(payment_change.status, '400 BAD REQUEST')

    def test_payment_change_status_responce_bad_json(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = {"s": "UPDATED"}
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id=payment.id),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertNotEqual(updated_payment.status, "UPDATED")
        self.assertEqual(payment_change.status, '400 BAD REQUEST')

    def test_payment_change_status_bad_payment_id(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id='97f65e39-e5cb-4b28-841d-8420f693bdbd'),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '404 NOT FOUND')

    def test_payment_change_status_bad_payment_id2(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id='lol'),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '404 NOT FOUND')

    def test_payment_change_status_bad_payment_id3(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        status = self.get_new_status()
        new_status = json.dumps(status)

        payment_change = self.client.put(
            self.api_base + '/payment/{payment_id}/status'.format(payment_id='nothing'),
            data=new_status,
            headers={"Content-Type": "application/json"}
        )
        updated_payment = Payment.query.filter_by(invoice_id=invoice_body['id']).one()

        self.assertEqual(payment_change.status, '404 NOT FOUND')