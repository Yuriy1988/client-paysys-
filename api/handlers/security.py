from api import app
from flask import jsonify, request
import re
import os

from api.errors import ValidationError, ServiceUnavailable


PUBLIC_KEY_FILE_NAME = 'public.pem'


def _is_valid_rsa_key(key):
    r = re.compile("^-----BEGIN PUBLIC KEY-----[A-Za-z0-9+=/\n]*-----END PUBLIC KEY-----$")
    return r.match(key)


@app.route('/api/client/dev/security/public_key', methods=['GET'])
def get_public_key():
    if not os.path.exists(PUBLIC_KEY_FILE_NAME):
        raise ServiceUnavailable("Key does not exist.")
    with open(PUBLIC_KEY_FILE_NAME) as f:
        public_key = f.read()
        key = {'key': public_key}
    return jsonify(key)


@app.route('/api/client/dev/security/public_key', methods=['POST'])
def upload_public_key():
    try:
        key_info = request.get_json()
        if 'key' not in key_info:
            raise ValidationError("'key' is required.")
        key = str(key_info['key'])
        if not _is_valid_rsa_key(key):
            raise ValidationError("Invalid key format.")
        with open(PUBLIC_KEY_FILE_NAME, 'w') as f:
            f.write(key)
    except TypeError:
        raise ValidationError("Set header. Content-Type: application/json")
    return jsonify({})
