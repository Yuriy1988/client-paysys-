import pika
from pika import exceptions as mq_err
from flask import json

from api import app, errors

__author__ = 'Kostel Serhii'


def _get_queue_connection_parameters():
    """
    Return pika connection parameters object.
    """
    return pika.ConnectionParameters(
        host=app.config["QUEUE_HOST"],
        port=app.config["QUEUE_PORT"],
        virtual_host=app.config["QUEUE_VIRTUAL_HOST"],
        credentials=pika.credentials.PlainCredentials(
            username=app.config["QUEUE_USERNAME"],
            password=app.config["QUEUE_PASSWORD"],
        )
    )


def push_to_queue(queue_name, body_json):
    """
    Open connection with queue,
    declare (pass if already declared) queue name and
    publish body message.

    Declare params:
        durable = True - restore messages after broker reboot
        exclusive = False - multiple connections
        auto_delete = False - do not delete after consumer cancels or disconnects

    Publish properties params:
        delivery_mode = 2 - make message persistent

    :param str queue_name: queue name
    :param dict body_json: message to push in queue
    """
    body = json.dumps(body_json)
    params = _get_queue_connection_parameters()
    publish_properties = pika.BasicProperties(content_type='text/plain', delivery_mode=2)

    try:

        with pika.BlockingConnection(params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)
            channel.basic_publish(exchange='', routing_key=queue_name, body=body, properties=publish_properties)

    except mq_err.AMQPConnectionError as err:
        raise errors.ServiceUnavailableError('Queue error: %r' % err)
    except (mq_err.AMQPChannelError, mq_err.AMQPError) as err:
        raise errors.InternalServerError('Queue error: %r' % err)