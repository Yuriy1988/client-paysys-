import os
from flask import jsonify, request, Response

from api import app
from api.errors import ServiceUnavailable, InternalServerError, ValidationError
from api.schemas.base import BaseSchema, Regexp, fields


class SecuritySchema(BaseSchema):

    key = fields.Str(required=True, validate=Regexp(
        regex='^-----BEGIN PUBLIC KEY-----[A-Za-z0-9+=/\n]*-----END PUBLIC KEY-----$',
        error='Wrong public key format.'))


@app.route('/api/client/dev/security/public_key', methods=['GET'])
def public_key_get():
    """
    Return public key from file.
    """
    if not os.path.exists(app.config["PUBLIC_KEY_FILE_NAME"]):
        raise ServiceUnavailable("RSA key does not exist.")

    try:
        with open(app.config["PUBLIC_KEY_FILE_NAME"]) as f:
            public_key = f.read()
    except IOError:
        raise InternalServerError('Read RSA public key error.')

    return jsonify(key=public_key)


@app.route('/api/client/dev/security/public_key', methods=['POST'])
def public_key_create():
    """
    Upload public key into file.
    """
    schema = SecuritySchema()
    data, errors = schema.load(request.get_json())
    if errors:
        raise ValidationError(errors=errors)

    try:
        with open(app.config["PUBLIC_KEY_FILE_NAME"], 'w') as f:
            f.write(data['key'])
    except IOError:
        raise InternalServerError('Error writing public key to file.')

    return Response(status=200)
