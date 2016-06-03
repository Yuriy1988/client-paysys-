from api import db
from api.models import Invoice, Payment, enum
import string
import random


class GenerateDB():

	currencies = enum.CURRENCY_ENUM
	store_ids = ['10', '13', '8', '11']
	pay_systems = enum.PAYMENT_SYSTEMS_ID_ENUM

	def __init__(self, new_items):
		for i in range(new_items):
			inv_dict = self.generate_invoice_dict()
			i = Invoice.create(inv_dict)
			db.session.commit()
			pay_dict = self.generate_pay_dict(i.id)
			p = Payment.create(pay_dict)
			db.session.commit()


	def generate_id(self, length):
		return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))


	def generate_number(self, length):
		return ''.join(random.choice(string.digits) for i in range(length))


	def generate_item(self):
		store_item_id = self.generate_id(5)
		quantity = random.randint(1, 10)
		unit_price = random.randint(100, 9999)/100
		return {'store_item_id': store_item_id, 'quantity': quantity, 'unit_price': unit_price}


	def generate_invoice_dict(self):
		order_id = self.generate_id(10)
		store_id = random.choice(self.store_ids)
		currency = random.choice(self.currencies)
		items = []
		for i in range(random.randint(1, 3)):
			items.append(self.generate_item())
		return {'order_id' : order_id, 'store_id': store_id, 'currency': currency, 'items': items}


	def generate_pay_dict(self, invoice_id):
		paysys_id = random.choice(self.pay_systems)
		payment_account = self.generate_number(16)
		crypted_payment = self.generate_id(10)
		return {'paysys_id': paysys_id, 'payment_account': payment_account, 'crypted_payment': crypted_payment, 'invoice_id': invoice_id}
