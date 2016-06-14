import logging
import jwt
import jwt.exceptions as jwt_err
from calendar import timegm
from datetime import datetime
from functools import wraps
from flask import g, request, current_app as app

from api import errors

__author__ = 'Kostel Serhii'


_log = logging.getLogger('xop.auth')


def _create_token(payload):
    token = jwt.encode(payload, app.config['AUTH_KEY'], algorithm=app.config['AUTH_ALGORITHM'])
    return token.decode('utf-8')


def _datetime_to_timestamp(dt_obj):
    """
    Convert datetime object to UTC UNIX timestamp.
    :param dt_obj: datetime object
    :return int: UTC UNIX timestamp
    """
    return timegm(dt_obj.utctimetuple())


# Auth decorator

def _check_authorization(access_groups, verify=False):
    """
    Check user authorisation and permissions.
    Save information about token and user_id into Flask.g storage.
    If access not allowed - raise api exceptions.

    Auth token in header:
        Authorization: Bearer <token>

    Check sequence:
        1. Token expired
        2. Session expired
        3. User access group
        4. IP address

    :param access_groups: user group or list of groups,
            that has permissions to make request for current rule
    :param verify: True/False - raise error if token expired or not
    """
    if isinstance(access_groups, str):
        access_groups = [access_groups]

    token_header = request.headers.get('Authorization', '').split()
    token = token_header[1] if len(token_header) == 2 and token_header[0] == 'Bearer' else None

    if not token:
        _log.warning('Token not found: %r', token_header)
        raise errors.UnauthorizedError('Token not found')

    try:
        payload = jwt.decode(token, app.config['AUTH_KEY'], verify=verify)
    except jwt_err.ExpiredSignatureError as err:
        _log.debug('Token expired: %r', err)
        raise errors.UnauthorizedError('Token expired')
    except jwt_err.InvalidTokenError as err:
        _log.warning('Wrong token: %r', err)
        raise errors.UnauthorizedError('Wrong token')

    groups = payload.get('groups', [])
    user_id = payload.get('user_id', '')

    if not (set(groups) & set(access_groups)):
        _log.warning('User %s not allowed to make such request. Need permissions: %r', user_id, access_groups)
        raise errors.ForbiddenError('Request forbidden for such role')

    if 'system' not in groups:
        session_exp = payload.get('session_exp', 0)
        ip_addr = payload.get('ip_addr', '')

        now = _datetime_to_timestamp(datetime.utcnow())
        if session_exp < now:
            _log.debug('Session %s expired', payload.get('session_id'))
            raise errors.UnauthorizedError('Session expired')

        remote_address = request.remote_addr
        if ip_addr != remote_address:
            _log.warning('Wrong IP: %s. Token created for IP: %s', remote_address, ip_addr)
            raise errors.ForbiddenError('Request forbidden from another network')

    g.token = token
    g.user_id = user_id


def auth(access_groups=None, verify=False):
    """
    A decorator that is used to check user authorization
    for access groups only::

        @auth
        def index():
            return 'Hi to All'

        @auth('admin'):
        def secret_code():
            return 42

        @auth(['admin', 'client'])
        def registered_only():
            return 'Hello User!'

    :param access_groups: user group or list of groups,
            that has permissions to make request for current rule.
            If None - do not check permission.
    :param verify: True/False - raise error if token expired or not
    """
    def auth_decorator(handler_method):

        @wraps(handler_method)
        def _handle_with_auth(*args, **kwargs):

            _check_authorization(access_groups, verify=verify)

            return handler_method(*args, **kwargs)

        return _handle_with_auth if access_groups is not None else handler_method

    return auth_decorator


# System

def get_system_token():
    """
    System token to communicate between internal services
    :return: system JWT token
    """
    payload = dict(
        exp=datetime.utcnow() + app.config['AUTH_TOKEN_LIFE_TIME'],
        user_id=app.config['AUTH_SYSTEM_USER_ID'],
        groups=['system'],
    )
    return _create_token(payload=payload)


def get_access_token():
    """
    Access token for temporary requests without authorization
    :return: access JWT token
    """
    payload = dict(
        exp=datetime.utcnow() + app.config['ACCESS_TOKEN_LIFE_TIME'],
        groups=['access_token'],
    )
    return _create_token(payload=payload)