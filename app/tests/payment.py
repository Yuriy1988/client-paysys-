from app.tests import base
from app.models import Payment

__author__ = 'Andrey Kupriy'


class TestPayment(base.BaseTestCase):

    # invoices/<invoice_id>/payments/visa_master

    def test_post_payment_full_valid_response(self):
        invoice = self.get_invoice()
        card_info = self.get_card_info()

        status, body = self.post('/invoices/{invoice_id}/payments/visa_master'.format(invoice_id=invoice.id), card_info)

        self.assertEqual(status, 200)
        # id generated:
        self.assertIn('id', body)
        # items created and added:
        self.assertIn('status', body)
