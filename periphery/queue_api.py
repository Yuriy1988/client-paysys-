import pika

from api import app
from periphery.service_error import handle_service_unavailable_error


@handle_service_unavailable_error(msg="RabbitMQ service is unavailable now.")
def push(body):
    # Connect to the queue server
    with pika.BlockingConnection(pika.ConnectionParameters(host=app.config["QUEUE_HOST_ADDRESS"])) as connection:
        channel = connection.channel()

        # Create a queue with QUEUE_NAME name
        channel.queue_declare(queue=app.config["QUEUE_NAME"])

        # Add "body" to QUEUE_NAME queue
        channel.basic_publish(exchange='',
                              routing_key=app.config["QUEUE_NAME"],
                              body=body)
        # print(" [x] Sent body: ", body)


@handle_service_unavailable_error(msg="RabbitMQ service is unavailable now.")
def pop():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=app.config["QUEUE_HOST_ADDRESS"]))
    channel = connection.channel()

    channel.queue_declare(queue=app.config["QUEUE_NAME"])

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                          queue=app.config["QUEUE_NAME"],
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
