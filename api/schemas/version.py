from marshmallow import fields

from api.schemas import base


class VersionSchema(base.BaseSchema):
    api_version = fields.Str(required=True)
    server_version = fields.Str(required=True)
    build_date = fields.DateTime(required=True)
