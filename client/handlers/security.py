from client import app
from config import CURRENT_CLIENT_SERVER_VERSION
from flask import jsonify, request, Response
import re
import os

from client.errors import ValidationError, NotFoundError


PUBLIC_KEY_FILE_NAME = 'public.pem'


def _is_valid_rsa_key(key):
    r = re.compile("^-----BEGIN PUBLIC KEY-----[A-Za-z0-9+=/\n]*-----END PUBLIC KEY-----$")
    return r.match(key)


@app.route('/api/client/{version}/public_key'.format(
    version=CURRENT_CLIENT_SERVER_VERSION), methods=['GET']
)
def get_public_key():
    if not os.path.exists(PUBLIC_KEY_FILE_NAME):
        raise NotFoundError("Key does not exist.")
    with open(PUBLIC_KEY_FILE_NAME) as f:
        public_key = f.read()
        key = {'key': public_key}
    return jsonify(key)


@app.route('/api/client/{version}/public_key'.format(
    version=CURRENT_CLIENT_SERVER_VERSION), methods=['POST']
)
def upload_public_key():
    key_info = request.get_json()
    if 'key' not in key_info:
        raise ValidationError("'key' is required.")
    key = str(key_info['key'])

    if not _is_valid_rsa_key(key):
        raise ValidationError("Invalid key format.")

    with open(PUBLIC_KEY_FILE_NAME, 'w') as f:
        f.write(key)

    return Response(status=200)