from datetime import datetime

from api import db
from api.models import Invoice, Payment
from api.tests import base


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
        self._create_invoice_db()

    def _create_invoice(self, order_id, store_id, currency, number_of_invoices,
                        paysys_id, items, payment_account, status, year):
        invoice = self.get_invoice()
        payment = self.get_payment()
        invoice['order_id'] = order_id
        invoice['store_id'] = store_id
        invoice['currency'] = currency
        invoice['items'] = items
        payment['payment_account'] = self.payment_base + payment_account
        payment['status'] = status # 'CREATED', 'ACCEPTED', 'SUCCESS', '3D_SECURE', 'REJECTED'
        payment['paysys_id'] = paysys_id

        invoices_models = [Invoice.create(invoice) for i in range(number_of_invoices)]
        db.session.commit()

        for inv in invoices_models:
            payment['invoice_id'] = inv.id
            pay = Payment.create(payment)
            pay.created = datetime(year=year, month=5, day=4, hour=11, minute=1)
            pay.updated = datetime(year=year, month=6, day=4, hour=11, minute=1)

        db.session.commit()

    def _create_items(self, price):
        return [{'store_item_id': 'aaa', 'quantity': 1, 'unit_price': price}]

    def _create_invoice_db(self):
        self._create_invoice('10', self.store_ids[0], 'UAH', 4, 'BIT_COIN', self._create_items(100), '0000', 'CREATED', 2015)
        self._create_invoice('20', self.store_ids[1], 'RUB', 5, 'PAY_PAL', self._create_items(200), '1111', 'ACCEPTED', 2014)
        self._create_invoice('30', self.store_ids[2], 'EUR', 6, 'VISA_MASTER', self._create_items(300), '2222', 'SUCCESS', 2016)
        self._create_invoice('40', self.store_ids[3], 'USD', 7, 'VISA_MASTER', self._create_items(400), '3333', 'REJECTED', 2013)

    def get(self, url, query_args=None, **kwargs):
        return super(TestStatistics, self).get(url=url, query_args=query_args, token=self.get_system_token())

    def test_statistics_get(self):
        status, body = self.get(self.url, query_args={'limit': 30})
        self.assertEqual(status, 200)
        self.assertEqual(body['count'], 22)

    def test_statistics_currency(self):
        status, body = self.get(self.url, query_args={'currency': 'UAH'})
        self.assertEqual(body['count'], 4)
        status, body = self.get(self.url, query_args={'currency': 'RUB'})
        self.assertEqual(body['count'], 5)
        status, body = self.get(self.url, query_args={'currency': 'EUR'})
        self.assertEqual(body['count'], 6)
        status, body = self.get(self.url, query_args={'currency': 'USD'})
        self.assertEqual(body['count'], 7)

    def test_statistics_store_id(self):
        status, body = self.get(self.url, query_args={'store_id': self.store_ids[0]})
        self.assertEqual(body['count'], 4)
        status, body = self.get(self.url, query_args={'store_id': self.store_ids[1]})
        self.assertEqual(body['count'], 5)
        status, body = self.get(self.url, query_args={'store_id': self.store_ids[2]})
        self.assertEqual(body['count'], 6)
        status, body = self.get(self.url, query_args={'store_id': self.store_ids[3]})
        self.assertEqual(body['count'], 7)

    def test_statistics_paysys_id(self):
        status, body = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'BIT_COIN'})
        self.assertEqual(body['count'], 4)
        status, body = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'VISA_MASTER'})
        self.assertEqual(body['count'], 13)
        status, body = self.get(self.url, query_args={'limit': 25, 'paysys_id': 'PAY_PAL'})
        self.assertEqual(body['count'], 5)

    def test_statistics_from_total_price(self):
        status, body = self.get(self.url, query_args={'from_total_price': 200, 'limit': 25})
        self.assertEqual(body['count'], 18)
        status, body = self.get(self.url, query_args={'from_total_price': 300, 'limit': 25})
        self.assertEqual(body['count'], 13)
        status, body = self.get(self.url, query_args={'from_total_price': 400, 'limit': 25})
        self.assertEqual(body['count'], 7)

    def test_statistics_till_total_price(self):
        status, body = self.get(self.url, query_args={'till_total_price': 100, 'limit': 25})
        self.assertEqual(body['count'], 4)
        status, body = self.get(self.url, query_args={'till_total_price': 200, 'limit': 25})
        self.assertEqual(body['count'], 9)
        status, body = self.get(self.url, query_args={'till_total_price': 300, 'limit': 25})
        self.assertEqual(body['count'], 15)

    def test_statistics_price_range(self):
        status, body = self.get(self.url, query_args={'from_total_price': 100, 'till_total_price': 200, 'limit': 25})
        self.assertEqual(body['count'], 9)
        status, body = self.get(self.url, query_args={'from_total_price': 200, 'till_total_price': 300, 'limit': 25})
        self.assertEqual(body['count'], 11)
        status, body = self.get(self.url, query_args={'from_total_price': 300, 'till_total_price': 400, 'limit': 25})
        self.assertEqual(body['count'], 13)

    def test_statistics_price_from_less_than_till(self):
        status, body = self.get(self.url, query_args={'from_total_price': 200, 'till_total_price': 100, 'limit': 25})
        self.assertEqual(status, 400)

    def test_statistics_payment_account(self):
        status, body = self.get(self.url, query_args={'payment_account': self.payment_base + '0000'})
        self.assertEqual(body['count'], 4)
        status, body = self.get(self.url, query_args={'payment_account': self.payment_base + '1111'})
        self.assertEqual(body['count'], 5)
        status, body = self.get(self.url, query_args={'payment_account': self.payment_base + '2222'})
        self.assertEqual(body['count'], 6)
        status, body = self.get(self.url, query_args={'payment_account': self.payment_base + '3333'})
        self.assertEqual(body['count'], 7)

    def test_statistics_status(self):
        status, body = self.get(self.url, query_args={'status': 'CREATED'})
        self.assertEqual(body['count'], 4)
        status, body = self.get(self.url, query_args={'status': 'ACCEPTED'})
        self.assertEqual(body['count'], 5)
        status, body = self.get(self.url, query_args={'status': 'SUCCESS'})
        self.assertEqual(body['count'], 6)
        status, body = self.get(self.url, query_args={'status': 'REJECTED'})
        self.assertEqual(body['count'], 7)

    def test_statistics_order_by(self):
        status, body = self.get(self.url, query_args={'limit': 30, 'order_by': 'store_id'})
        self.assertEqual(body['payments'][0]['invoice']['store_id'], self.store_ids[0])
        self.assertEqual(body['payments'][5]['invoice']['store_id'], self.store_ids[1])
        self.assertEqual(body['payments'][11]['invoice']['store_id'], self.store_ids[2])
        self.assertEqual(body['payments'][20]['invoice']['store_id'], self.store_ids[3])
        status, body = self.get(self.url, query_args={'limit': 30, 'order_by': 'paysys_id'})
        self.assertEqual(body['payments'][1]['paysys_id'], 'PAY_PAL')
        self.assertEqual(body['payments'][7]['paysys_id'], 'BIT_COIN')
        self.assertEqual(body['payments'][18]['paysys_id'], 'VISA_MASTER')

    def test_statistics_from_date(self):
        status, body = self.get(self.url, query_args={'limit': 30, 'from_date': '2013-05-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 22)
        status, body = self.get(self.url, query_args={'limit': 30, 'from_date': '2014-05-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 15)
        status, body = self.get(self.url, query_args={'limit': 30, 'from_date': '2015-05-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 10)
        status, body = self.get(self.url, query_args={'limit': 30, 'from_date': '2016-05-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 6)

    def test_statistics_till_date(self):
        status, body = self.get(self.url, query_args={'limit': 30, 'till_date': '2013-06-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 7)
        status, body = self.get(self.url, query_args={'limit': 30, 'till_date': '2014-06-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 12)
        status, body = self.get(self.url, query_args={'limit': 30, 'till_date': '2015-06-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 16)
        status, body = self.get(self.url, query_args={'limit': 30, 'till_date': '2016-06-04T08:01:00+00:00'})
        self.assertEqual(body['count'], 22)

    def test_statistics_from_and_till_date(self):
        query = {'limit': 30, 'from_date': '2012-05-04T08:01:00+00:00', 'till_date': '2016-06-04T08:01:00+00:00'}
        status, body = self.get(self.url, query_args=query)
        self.assertEqual(body['count'], 22)

        query = {'limit': 30, 'from_date': '2014-05-04T08:01:00+00:00', 'till_date': '2015-06-04T08:01:00+00:00'}
        status, body = self.get(self.url, query_args=query)
        self.assertEqual(body['count'], 9)

    def test_statistics_from_less_than_till_date(self):
        query = {'from_date': '2015-05-04T08:01:00+00:00', 'till_date': '2013-06-04T08:01:00+00:00'}
        status, body = self.get(self.url, query_args=query)
        self.assertEqual(status, 400)

    def test_statistict_total_count_empty(self):
        status, body = self.get(self.url, query_args={'status': '3D_SECURE'})

        self.assertEqual(status, 200)
        self.assertEqual(body['count'], 0)
        self.assertEqual(body['total_count'], 0)

    def test_statistict_total_count(self):
        status, body = self.get(self.url, query_args={'limit': 10})

        self.assertEqual(status, 200)
        self.assertEqual(body['count'], 10)
        self.assertEqual(body['total_count'], Payment.query.count())
