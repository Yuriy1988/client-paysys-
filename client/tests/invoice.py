from client.tests import base
from client.models import Invoice

__author__ = 'Andrey Kupriy'


class TestInvoice(base.BaseTestCase):

    # POST /invoices

    def test_post_invoice_full_valid_response(self):
        invoice = self.get_invoice()

        status, body = self.post('/invoices', invoice)

        self.assertEqual(status, 200)
        self.assertIn('id', body)
        self.assertIn('items', body)
        self.assertIn('order_id', body)
        self.assertIn('store_id', body)
        self.assertIn('currency', body)

    def test_post_invoice_with_no_order_id(self):
        invoice = self.get_invoice()
        del invoice['order_id']

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_with_no_store_id(self):
        invoice = self.get_invoice()
        del invoice['store_id']

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_with_int_store_id(self):
        invoice = self.get_invoice()
        invoice['store_id'] = 10

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_with_no_currency(self):
        invoice = self.get_invoice()
        del invoice['currency']

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_with_wrong_currency(self):
        invoice = self.get_invoice()
        invoice['currency'] = "US"

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_with_wrong_currency_2(self):
        invoice = self.get_invoice()
        invoice['currency'] = "USDU"

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_create_no_items_in_model(self):
        invoice = self.get_invoice()
        invoice['items'] = None

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_create_0_items_quantity(self):
        invoice = self.get_invoice()
        for item in invoice['items']:
            item['quantity'] = 0

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_create_no_items_price(self):
        invoice = self.get_invoice()
        for item in invoice['items']:
            item['unit_price'] = None

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_create_wrong_items_price(self):
        invoice = self.get_invoice()
        for item in invoice['items']:
            item['unit_price'] = ''

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_create_letter_items_price(self):
        invoice = self.get_invoice()
        for item in invoice['items']:
            item['unit_price'] = 'sdas'

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_create_letter_items_quantity(self):
        invoice = self.get_invoice()
        for item in invoice['items']:
            item['quantity'] = 'sd'

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 400)

    def test_post_invoice_created(self):
        invoice = self.get_invoice()

        status, body = self.post('/invoices', invoice)
        self.assertEqual(status, 200)

        # invoice created
        invoice_model = Invoice.query.filter_by(id=body['id']).first()
        self.assertEqual(body['id'], invoice_model.id)

    # GET /invoices/<id>

    def test_get_invoice_not_found(self):
        invoice = self.get_invoice()
        status, body = self.post('/invoices', invoice)

        status, body = self.get('/invoices/0')
        self.assertEqual(status, 404)

        status, body = self.get('/invoices/2')
        self.assertEqual(status, 404)

        status, body = self.get('/invoices/test')
        self.assertEqual(status, 404)

        status, body = self.get('/invoices/null')
        self.assertEqual(status, 404)

        status, body = self.get('/invoices/')
        self.assertEqual(status, 404)

    def test_get_invoice_by_id(self):
        invoice = self.get_invoice()
        status1, body1 = self.post('/invoices', invoice)
        status2, body2 = self.post('/invoices', invoice)
        invoice_model_1 = Invoice.query.get(body1['id'])
        invoice_model_2 = Invoice.query.get(body2['id'])

        status, body = self.get('/invoices/{id}'.format(id=invoice_model_1.id))
        self.assertEqual(status, 200)

        status, body = self.get('/invoices/{id}'.format(id=invoice_model_2.id))
        self.assertEqual(status, 200)

    def test_get_invoice_full_valid_response(self):
        invoice = self.get_invoice()
        status, body = self.post('/invoices', invoice)
        invoice_model = Invoice.query.get(body['id'])

        status, body = self.get('/invoices/{id}'.format(id=invoice_model.id))
        self.assertEqual(status, 200)

        self.assertIn('id', body)
        self.assertIn('order_id', body)
        self.assertIn('store_id', body)
        self.assertIn('currency', body)
        self.assertIn('items', body)
        for item in body['items']:
            self.assertIn('store_item_id', item)
            self.assertIn('quantity', item)
            self.assertIn('unit_price', item)
            self.assertIn('item_name', item)

