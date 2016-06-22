import pytz
import pika
import logging
import requests
from datetime import datetime
from pika import exceptions as mq_err
from requests import exceptions
from flask import g, current_app as app, json, request

from api import after_app_created, errors, auth, helper
from api.schemas import InvoiceSchema

__author__ = 'Kostel Serhii'


_log = logging.getLogger('xop.utils')


# Queue

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


# Admin service

def _admin_server_get_request(url, **params):
    """
    Make request to admin server and return response.
    :param url: url (without base prefix) to admin server
    :param params: url parameters
    :return: response as dict or raise exception
    """
    full_url = app.config["ADMIN_API_URL"] + url
    headers = {"Authorization": "Bearer %s" % auth.get_system_token()}

    try:
        response = requests.get(full_url, params=params, headers=headers, timeout=5)

    except exceptions.Timeout:
        raise errors.ServiceUnavailableError('The admin server connection timeout.')
    except exceptions.ConnectionError:
        raise errors.ServiceUnavailableError('The admin server connection error.')
    except exceptions.RequestException:
        raise errors.InternalServerError('The admin server request error.')

    if response.status_code not in [200, 201, 202, 204]:
        raise errors.InternalServerError('Wrong response status {0} from admin server.'.format(response.status_code))

    try:
        data = response.json()
    except ValueError:
        raise errors.InternalServerError('Wrong response from admin server.')

    return data


def get_allowed_store_paysys(store_id):
    """
    Request store paysys, filter and return allowed only.
    :param store_id: store identifier
    :return: list of allowed paysys_id
    """
    resp = _admin_server_get_request('/stores/{id}/store_paysys'.format(id=store_id), allowed=True)
    store_paysys_list = resp.get('store_paysys', [])
    return [sps['paysys_id'] for sps in store_paysys_list]


def check_store_exists(store_id):
    """
    Request to check is store with store_id exists or not.
    :param store_id: store identifier
    :return: True/False - store exists or not
    """
    resp = _admin_server_get_request('/stores/{id}/exists'.format(id=store_id))
    return resp.get('exists', False)


def get_store(store_id):
    """
    Request store model json by store_id
    :param store_id: store identifier
    :return: dict with Store object
    """
    return _admin_server_get_request('/stores/{id}'.format(id=store_id))


def get_merchant_account(merchant_id):
    """
    Request merchant account model json by store_id
    :param merchant_id: merchant identifier
    :return: dict with Merchant Account object
    """
    merchant = _admin_server_get_request('/merchants/{id}'.format(id=merchant_id))
    return merchant['merchant_account']


def get_merchant_contracts(merchant_id, currency):
    """
    Request merchant contracts filtered by currency and active=True
    :param merchant_id: merchant identifier
    :param currency: one of currency enum
    :return: list with Merchant Contracts
    """
    resp = _admin_server_get_request('/merchants/{id}/contracts'.format(id=merchant_id),
                                     currency=currency, active=True)
    return resp.get('contracts', [])


def get_payment_system_contracts(paysys_id, currency):
    """
    Request payment system contracts filtered by currency and active=True
    :param paysys_id: payment system identifier
    :param currency: one of currency enum
    :return: list with Payment System Contracts
    """
    resp = _admin_server_get_request('/payment_systems/{id}/contracts'.format(id=paysys_id),
                                     currency=currency, active=True)
    return resp.get('contracts', [])


# Notify service

def _send_notify(queue_name, body_json):
    """
    Send notification task to the Notify Service through the queue.
    :param queue_name: notification queue name
    :param dict body_json: notification body json
    """
    _log.info("Send notification to [%s]: %r", queue_name,  body_json)
    try:
        push_to_queue(queue_name, body_json)
    except Exception as err:
        # Notification error should not crash task execution
        _log.error("Notification service is unavailable now: %s" % str(err))


def send_email(email_address, subject, message):
    """
    Send email notification.
    :param str email_address: email address
    :param str subject: email subject
    :param str message: email main message
    """
    _send_notify(app.config['QUEUE_EMAIL'], {'email_to': email_address, 'subject': subject, 'text': message})


def send_sms(phone_number, message):
    """
    Send sms notification.
    :param str phone_number: phone number
    :param str message: sms message
    """
    _send_notify(app.config['QUEUE_SMS'], {'phone': phone_number, 'text': message})


def add_track_extra_info(extra_info):
    """
    Add extra information into track extra info storage.
    :param dict extra_info: dict with extra information to track
    """
    if 'track_extra_info' not in g:
        g.track_extra_info = {}
    g.track_extra_info.update(extra_info)


@after_app_created
def register_request_notifier(app):
    """
    Register request notifier.
    :param app: Flask application
    """
    if not app.config.get('AFTER_REQUEST_TRACK_ENABLE'):
        return

    filtered_headers = ['HTTP_USER_AGENT', 'CONTENT_LENGTH', 'CONTENT_TYPE']

    @app.after_request
    def track_request(response):
        """
        After every request send information to the notify queue
        to monitor and send alerts depending on the request information.
        :param response: request response
        """
        request_detail = dict(
            service_name=app.config['SERVICE_NAME'],

            query=dict(
                timestamp=datetime.now(tz=pytz.utc),
                path=request.full_path if request.query_string else request.path,
                method=request.method,
                status_code=response.status_code,
                remote_address=request.remote_addr,
                view_args=request.view_args,
                headers={k: v for k, v in request.headers.environ.items() if k in filtered_headers},
            ),

            user=dict(
                id=g.get('user_id'),
                name=g.get('user_name'),
                ip_addr=g.get('user_ip_addr'),
                groups=g.get('groups'),
            ),

            extra=g.get('track_extra_info', {})
        )

        _send_notify(app.config['QUEUE_REQUEST'], request_detail)

        return response


# Processing service

def send_transaction(invoice, payment):
    """
    Collect all necessary information about transaction
    and send this object to queue.
    :param invoice: Invoice model instance
    :param payment: Payment model instance
    """
    invoice_json = InvoiceSchema().dump(invoice)

    store = get_store(invoice.store_id)
    merchant_id = store['merchant_id']
    merchant_account_json = get_merchant_account(merchant_id)

    route = helper.get_route(payment.paysys_id, merchant_id, invoice.total_price, invoice.currency)

    transaction = {
        "id": payment.id,
        "payment": {
            "description": payment.description or "Payment for order {id}".format(id=invoice.order_id),
            "invoice": invoice_json,
            "amount_coins": invoice.total_price_coins,
        },
        "source": {
            "paysys_contract": route.paysys_contract,
            "payment_requisites": {
                "crypted_payment": payment.crypted_payment
            }
        },
        "destination": {
            "merchant_contract": route.merchant_contract,
            "merchant_account": merchant_account_json
        }
    }

    _log.info('Send transaction [%s] to queue', payment.id)

    push_to_queue(app.config['QUEUE_TRANS_FOR_PROCESSING'], transaction)


def send_3d_secure_result(trans_id, status, extra_info):
    """
    Send result of the 3D secure to queue.
    :param trans_id: transaction identifier
    :param status: status of the 3D secure operation
    :param extra_info: additional information from 3D server
    """
    result_3d_secure = {
        "trans_id": trans_id,
        "status": status,
        "extra_info": extra_info
    }

    _log.info('Send 3D secure result [%s] to queue', str(result_3d_secure))

    push_to_queue(app.config['QUEUE_3D_SECURE_RESULT'], result_3d_secure)
