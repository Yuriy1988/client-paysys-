import jwt
from datetime import datetime

from api import app

__author__ = 'Kostel Serhii'


def _create_token(payload):
    token = jwt.encode(payload, app.config['AUTH_KEY'], algorithm=app.config['AUTH_ALGORITHM'])
    return token.decode('utf-8')


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
