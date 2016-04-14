import pika

from api import app
from periphery.service_error import handle_service_unavailable_error


def get_connection_parameters():
    return pika.ConnectionParameters(
        host=app.config["QUEUE_HOST"],
        port=app.config["QUEUE_PORT"],
        virtual_host=app.config["QUEUE_VIRTUAL_HOST"],
        credentials=pika.credentials.PlainCredentials(
            username=app.config["QUEUE_USERNAME"],
            password=app.config["QUEUE_PASSWORD"],
        )
    )


@handle_service_unavailable_error(msg="RabbitMQ service is unavailable now.")
def push(body):
    with pika.BlockingConnection(get_connection_parameters()) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=app.config["QUEUE_NAME"], durable=True, exclusive=True, auto_delete=False)
        channel.basic_publish(exchange='', routing_key=app.config["QUEUE_NAME"], body=body,
                              properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2))

