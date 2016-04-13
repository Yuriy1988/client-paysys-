import pika

from api import app
from periphery.service_error import handle_service_unavailable_error


def callback(ch, method, properties, body):
    print(body)


def get_connection_parameters():
    return pika.ConnectionParameters(
        host=app.config["QUEUE_HOST"],
        port=app.config["QUEUE_PORT"],
        credentials=pika.credentials.PlainCredentials(
            username=app.config["QUEUE_USERNAME"],
            password=app.config["QUEUE_PASSWORD"],
        )
    )


@handle_service_unavailable_error(msg="RabbitMQ service is unavailable now.")
def push(body):
    with pika.BlockingConnection(get_connection_parameters()) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=app.config["QUEUE_NAME"])
        channel.basic_publish(exchange='',
                              routing_key=app.config["QUEUE_NAME"],
                              body=body)


@handle_service_unavailable_error(msg="RabbitMQ service is unavailable now.")
def pop():
    connection = pika.BlockingConnection(get_connection_parameters())
    channel = connection.channel()
    channel.queue_declare(queue=app.config["QUEUE_NAME"])

    channel.basic_consume(callback,
                          queue=app.config["QUEUE_NAME"],
                          no_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    app.config.from_object('config.Debug')
    push("Hello")
    pop()
