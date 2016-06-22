from api.models import Invoice, Payment
from api.tests import base
import unittest
from datetime import datetime
from api import db

class TestStatistics(base.BaseTestCase):

    url = '/statistics/payments'
    store_ids = ['00000000-0000-0000-0000-000000000000',
                 '11111111-1111-1111-1111-111111111111',
                 '22222222-2222-2222-2222-222222222222',
                 '33333333-3333-3333-3333-333333333333']
    payment_base = '412398760123'
    setup_done = False

    def setUp(self):
        super(TestStatistics, self).setUp()
        self.create_db()

    def create_invoice(self, order_id, store_id, currency, number_of_invoices, paysys_id, items, payment_account, status, year):
        invoice = self.get_invoice()
        payment = self.get_payment()
        invoice['order_id'] = order_id
        invoice['store_id'] = store_id
        invoice['currency'] = currency
        invoice['items'] = items
        payment['payment_account'] = self.payment_base + payment_account
        payment['status'] = status # 'CREATED', 'ACCEPTED', 'SUCCESS', '3D_SECURE', 'REJECTED'
        payment['paysys_id'] = paysys_id

        for i in range(number_of_invoices):
            inv = Invoice.create(invoice)
            db.session.commit()
            payment['invoice_id'] = inv.id
            pay = Payment.create(payment)
            pay.created = datetime(year=year, month=5, day=4, hour=11, minute=1)
            pay.updated = datetime(year=year, month=6, day=4, hour=11, minute=1)

        db.session.commit()

    def create_db(self):
        self.create_invoice('10', self.store_ids[0], 'UAH', 4, 'BIT_COIN', self.create_items(100), '0000', 'CREATED', 2015)
        self.create_invoice('20', self.store_ids[1], 'RUB', 5, 'PAY_PAL', self.create_items(200), '1111', 'ACCEPTED', 2014)
        self.create_invoice('30', self.store_ids[2], 'EUR', 6, 'VISA_MASTER', self.create_items(300), '2222', 'SUCCESS', 2016)
        self.create_invoice('40', self.store_ids[3], 'USD', 7, 'VISA_MASTER', self.create_items(400), '3333', 'REJECTED', 2013)

    def create_items(self, price):
        return [{'store_item_id': 'aaa', 'quantity': 1, 'unit_price': price}]

    def get(self, url, query_args=None, **kwargs):
        return super(TestStatistics, self).get(url=url, query_args=query_args, token=self.get_system_token())

    def test_statistics_get(self):
        p = self.get(self.url, query_args={'limit': 30})
        self.assertEqual(p[0], 200)
        self.assertEqual(p[1]['count'], 22)

    def test_statistics_currency(self):
        p = self.get(self.url, query_args={'currency': 'UAH'})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'currency': 'RUB'})
        self.assertEqual(p[1]['count'], 5)
        p = self.get(self.url, query_args={'currency': 'EUR'})
        self.assertEqual(p[1]['count'], 6)
        p = self.get(self.url, query_args={'currency': 'USD'})
        self.assertEqual(p[1]['count'], 7)

    def test_statistics_store_id(self):
        p = self.get(self.url, query_args={'store_id': self.store_ids[0]})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'store_id': self.store_ids[1]})
        self.assertEqual(p[1]['count'], 5)
        p = self.get(self.url, query_args={'store_id': self.store_ids[2]})
        self.assertEqual(p[1]['count'], 6)
        p = self.get(self.url, query_args={'store_id': self.store_ids[3]})
        self.assertEqual(p[1]['count'], 7)

    def test_statistics_paysys_id(self):
        p = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'BIT_COIN'})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'VISA_MASTER'})
        self.assertEqual(p[1]['count'], 13)
        p = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'PAY_PAL'})
        self.assertEqual(p[1]['count'], 5)

    def test_statistics_from_total_price(self):
        p = self.get(self.url, query_args={'from_total_price': 200, 'limit': 25})
        self.assertEqual(p[1]['count'], 18)
        p = self.get(self.url, query_args={'from_total_price': 300, 'limit': 25})
        self.assertEqual(p[1]['count'], 13)
        p = self.get(self.url, query_args={'from_total_price': 400, 'limit': 25})
        self.assertEqual(p[1]['count'], 7)

    def test_statistics_till_total_price(self):
        p = self.get(self.url, query_args={'till_total_price': 100, 'limit': 25})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'till_total_price': 200, 'limit': 25})
        self.assertEqual(p[1]['count'], 9)
        p = self.get(self.url, query_args={'till_total_price': 300, 'limit': 25})
        self.assertEqual(p[1]['count'], 15)

    def test_statistics_payment_account(self):
        p = self.get(self.url, query_args={'payment_account': self.payment_base + '0000'})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'payment_account': self.payment_base + '1111'})
        self.assertEqual(p[1]['count'], 5)
        p = self.get(self.url, query_args={'payment_account': self.payment_base + '2222'})
        self.assertEqual(p[1]['count'], 6)
        p = self.get(self.url, query_args={'payment_account': self.payment_base + '3333'})
        self.assertEqual(p[1]['count'], 7)

    def test_statistics_status(self):
        p = self.get(self.url, query_args={'status': 'CREATED'})
        self.assertEqual(p[1]['count'], 4)
        p = self.get(self.url, query_args={'status': 'ACCEPTED'})
        self.assertEqual(p[1]['count'], 5)
        p = self.get(self.url, query_args={'status': 'SUCCESS'})
        self.assertEqual(p[1]['count'], 6)
        p = self.get(self.url, query_args={'status': 'REJECTED'})
        self.assertEqual(p[1]['count'], 7)

    def test_statistics_order_by(self):
        p = self.get(self.url, query_args={'limit': 30, 'order_by': 'store_id'})
        self.assertEqual(p[1]['payments'][0]['invoice']['store_id'], self.store_ids[0])
        self.assertEqual(p[1]['payments'][5]['invoice']['store_id'], self.store_ids[1])
        self.assertEqual(p[1]['payments'][11]['invoice']['store_id'], self.store_ids[2])
        self.assertEqual(p[1]['payments'][20]['invoice']['store_id'], self.store_ids[3])
        p = self.get(self.url, query_args={'limit': 30, 'order_by': 'paysys_id'})
        self.assertEqual(p[1]['payments'][1]['paysys_id'], 'PAY_PAL')
        self.assertEqual(p[1]['payments'][7]['paysys_id'], 'BIT_COIN')
        self.assertEqual(p[1]['payments'][18]['paysys_id'], 'VISA_MASTER')

    def test_statistics_from_date(self):
        p = self.get(self.url, query_args={'limit': 30, 'from_date': '2013-05-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 22)
        p = self.get(self.url, query_args={'limit': 30, 'from_date': '2014-05-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 15)
        p = self.get(self.url, query_args={'limit': 30, 'from_date': '2015-05-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 10)
        p = self.get(self.url, query_args={'limit': 30, 'from_date': '2016-05-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 6)

    def test_statistics_till_date(self):
        p = self.get(self.url, query_args={'limit': 30, 'till_date': '2013-06-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 22)
        p = self.get(self.url, query_args={'limit': 30, 'till_date': '2014-06-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 15)
        p = self.get(self.url, query_args={'limit': 30, 'till_date': '2015-06-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 10)
        p = self.get(self.url, query_args={'limit': 30, 'till_date': '2016-06-04T08:01:00+00:00'})
        self.assertEqual(p[1]['count'], 6)


if __name__ == '__main__':
    unittest.main()