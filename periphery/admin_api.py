import requests
from requests import exceptions

from api import app, errors


def _admin_server_get_request(url, **params):
    """
    Make request to admin server and return response.
    :param url: url (without base prefix) to admin server
    :param params: url parameters
    :return: response as dict or raise exception
    """
    full_url = app.config["ADMIN_API_URL"] + url
    try:
        response = requests.get(full_url, params=params, timeout=5)

    except exceptions.Timeout:
        raise errors.ServiceUnavailable('The admin server connection timeout.')

    except exceptions.ConnectionError:
        raise errors.ServiceUnavailable('The admin server connection error.')

    except exceptions.RequestException:
        raise errors.InternalServerError('The admin server request error.')

    if response.status_code == requests.codes.ok:
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


def get_merchant(merchant_id):
    """
    Request merchant model json by store_id
    :param merchant_id: merchant identifier
    :return: dict with Merchant object
    """
    return _admin_server_get_request('/merchants/{id}'.format(id=merchant_id))


def get_merchant_contracts(merchant_id, currency):
    """
    Request merchant contracts filtered by currency and active=True
    :param merchant_id: merchant identifier
    :param currency: one of currency enum
    :return: dict with Merchant Contracts
    """
    return _admin_server_get_request('/merchants/{id}/contracts'.format(id=merchant_id),
                                     currency=currency, active=True)


def get_payment_system_contracts(paysys_id, currency):
    """
    Request payment system contracts filtered by currency and active=True
    :param paysys_id: payment system identifier
    :param currency: one of currency enum
    :return: dict with Merchant Contracts
    """
    return _admin_server_get_request('/payment_systems/{id}/contracts'.format(id=paysys_id),
                                     currency=currency, active=True)
