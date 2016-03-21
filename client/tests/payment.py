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

        #self.assertEqual(payment_status, 200)
        # payment id generated:
        self.assertIn('id', payment_body)
        # status added:
        self.assertIn('status', payment_body)

    def test_payment_saved_to_db(self):
        invoice = self.get_invoice()
        invoice_status, invoice_body = self.post('/invoices', invoice)

        card_info = self.get_card_info()
        payment_status, payment_body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(
            invoice_id=invoice_body['id']), card_info)

        invoice = Invoice.query.get(invoice_body['id'])
        payment = Payment.query.filter_by(invoice_id=invoice.id)

        self.assertIsNotNone(payment)
