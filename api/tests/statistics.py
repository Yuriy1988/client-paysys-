from api.models import Invoice, Payment
from api.tests import base
import unittest
from api import db


class TestStatistics(base.BaseTestCase):

    url = '/statistics/payments'
    store_ids = ['00000000-0000-0000-0000-000000000000',
                 '11111111-1111-1111-1111-111111111111',
                 '22222222-2222-2222-2222-222222222222',
                 '33333333-3333-3333-3333-333333333333']

    def setUp(self):
        super(TestStatistics, self).setUp()
        self.create_db()

    def create_invoice(self, order_id, store_id, currency, number_of_invoices, paysys_id, items):
        invoice = self.get_invoice()
        payment = self.get_payment()
        invoice['order_id'] = order_id
        invoice['store_id'] = store_id
        invoice['currency'] = currency
        invoice['items'] = items

        for i in range(number_of_invoices):
            inv = Invoice.create(invoice)
            db.session.commit()
            payment['invoice_id'] = inv.id
            payment['paysys_id'] = paysys_id
            pay = Payment.create(payment)
            db.session.commit()

    def create_db(self):
        self.create_invoice('10', self.store_ids[0], 'UAH', 4, 'PAY_PAL', self.create_items(100))
        self.create_invoice('20', self.store_ids[1], 'RUB', 5, 'VISA_MASTER', self.create_items(200))
        self.create_invoice('30', self.store_ids[2], 'EUR', 6, 'BIT_COIN', self.create_items(300))
        self.create_invoice('40', self.store_ids[3], 'USD', 7, 'VISA_MASTER', self.create_items(400))

    def create_items(self, price):
        return [{'store_item_id': 'aaa', 'quantity': 1, 'unit_price': price}]

    def get(self, url, query_args=None, **kwargs):
        return super(TestStatistics, self).get(url=url, query_args=query_args, token=self.get_system_token())

    def test_get(self):
        p = self.get(self.url, query_args={'limit': 30})
        self.assertEqual(p[0], 200)
        self.assertEqual(p[1]['count'], 22)

    def test_currency(self):
        p = self.get(self.url, query_args={'currency': 'UAH'})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'currency': 'RUB'})
        self.assertEqual(p[1]['count'], 5)
        p = self.get(self.url, query_args={'currency': 'EUR'})
        self.assertEqual(p[1]['count'], 6)
        p = self.get(self.url, query_args={'currency': 'USD'})
        self.assertEqual(p[1]['count'], 7)

    def test_store_id(self):
        p = self.get(self.url, query_args={'store_id': self.store_ids[0]})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'store_id': self.store_ids[1]})
        self.assertEqual(p[1]['count'], 5)
        p = self.get(self.url, query_args={'store_id': self.store_ids[2]})
        self.assertEqual(p[1]['count'], 6)
        p = self.get(self.url, query_args={'store_id': self.store_ids[3]})
        self.assertEqual(p[1]['count'], 7)

    def test_paysys_id(self):
        p = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'PAY_PAL'})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'VISA_MASTER'})
        self.assertEqual(p[1]['count'], 12)
        p = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'BIT_COIN'})
        self.assertEqual(p[1]['count'], 6)

    def test_from_total_price(self):
        p = self.get(self.url, query_args={'from_total_price': 200, 'limit': 25})
        self.assertEqual(p[1]['count'], 18)
        p = self.get(self.url, query_args={'from_total_price': 300, 'limit': 25})
        self.assertEqual(p[1]['count'], 13)
        p = self.get(self.url, query_args={'from_total_price': 400, 'limit': 25})
        self.assertEqual(p[1]['count'], 7)

    def test_till_total_price(self):
        p = self.get(self.url, query_args={'till_total_price': 100, 'limit': 25})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'till_total_price': 200, 'limit': 25})
        self.assertEqual(p[1]['count'], 9)
        p = self.get(self.url, query_args={'till_total_price': 300, 'limit': 25})
        self.assertEqual(p[1]['count'], 15)


if __name__ == '__main__':
    unittest.main()