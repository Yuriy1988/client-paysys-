from marshmallow import Schema as _Schema, fields, ValidationError, validates_schema

__author__ = 'Kostel Serhii'


class BaseSchema(_Schema):

    def __init__(self, *args, **kwargs):
        partial_nested = kwargs.pop('partial_nested', False)
        super().__init__(*args, **kwargs)
        if partial_nested:
            self._make_partial_nested()

    def _make_partial_nested(self):
        # FIXME: duty hack. Make it right
        for attr_name, value in self.__dict__.items():
            if attr_name[0] != '_' and isinstance(value, fields.Nested):
                setattr(value, 'partial', True)

    @validates_schema
    def validate_not_none(self, data):
        if data is None:
            raise ValidationError('Content-Type header missing')
