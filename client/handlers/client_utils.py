from config import ADMIN_URL, CURRENT_ADMIN_API_VERSION, QUEUE_HOST_ADDRESS, QUEUE_NAME
import requests
import decimal
import json
import pika


def put_to_queue(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST_ADDRESS))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=body)
    print(" [x] Sent 'Hello World!'")
    connection.close()
    return "ACCEPTED"


def get_store_by_store_id(store_id):
    url = '{admin_url}/api/admin/{current_admin_api_version}/info/stores/{store_id}'.format(
        admin_url=ADMIN_URL,
        current_admin_api_version=CURRENT_ADMIN_API_VERSION,
        store_id=store_id
    )
    return requests.get(url)


def mask_card_number(number):
    first_6 = number[0:6]
    last_4 = number[-4:]
    stars = '*' * (len(number) - 10)
    return '{first_6}{stars}{last_4}'.format(
        first_6=first_6,
        stars=stars,
        last_4=last_4
    )


def get_amount(items_list):
    amount = 0
    for item in items_list:
        amount += decimal.Decimal(item.unit_price) * int(item.quantity)
    return round(amount, 2)
