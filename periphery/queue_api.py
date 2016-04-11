import pika
from config import QUEUE_HOST_ADDRESS, QUEUE_NAME


def push(body):
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


def pop():
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
