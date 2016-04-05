from config import ADMIN_URL, CURRENT_ADMIN_SERVER_VERSION, QUEUE_HOST_ADDRESS, QUEUE_NAME, NOTIFICATION_SERVER_URL
import requests
import decimal
import pika
from celery import Celery


def send_email(email, subject, message):
    Celery(broker=NOTIFICATION_SERVER_URL).send_task('notify.send_mail', (email, subject, message))
    return "Message sent to {email}".format(email=email)


def put_to_queue(body):
    # Connect to the queue server
    with pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST_ADDRESS)) as connection:
        channel = connection.channel()

        # Create a queue with QUEUE_NAME name
        channel.queue_declare(queue=QUEUE_NAME)

        # Add "body" to QUEUE_NAME queue
        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME,
                              body=body)
        # print(" [x] Sent body: ", body)

    return "ACCEPTED"


def get_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST_ADDRESS))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue=QUEUE_NAME,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    pass


def get_store_by_store_id(store_id):
    url = '{admin_url}/api/admin/{current_admin_server_version}/stores/{store_id}'.format(
        admin_url=ADMIN_URL,
        current_admin_server_version=CURRENT_ADMIN_SERVER_VERSION,
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
