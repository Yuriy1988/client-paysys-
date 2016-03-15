from marshmallow import Schema as _Schema, fields, ValidationError, validates_schema
from marshmallow.validate import Validator as _Validator, Regexp

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


# Validators


class Unique(_Validator):
    """
    Validator which succeeds if the value passed to it is unique for specified model field.

    :param db.Model model: Database model class.
    :param str field_name: Name of the field in model, that will be checked.
    :param str error: Error message to raise in case of a validation error.
    """
    message = 'Field {field_name} must be unique.'

    def __init__(self, model, field_name, error=None):
        self.model = model
        self.field_name = field_name
        self.error = error

    def _repr_args(self):
        return 'model={0}, field_name={1}'.format(self.model, self.field_name)

    def _format_error(self, value, message):
        return (self.error or message).format(input=value, field_name=self.field_name)

    def __call__(self, value):
        if not self.model.check_unique(self.field_name, value):
            raise ValidationError(self._format_error(value, self.message))

        return value


class Phone(Regexp):

    default_message = 'Wrong phone format.'
    default_regex = '^[1-9]{1}[0-9]{3,14}$'

    def __init__(self, **kwargs):
        regex = kwargs.pop('regex', self.default_regex)
        super().__init__(regex, **kwargs)


class FixedDigitsNum(Regexp):

    default_message = 'Value must contains exactly {num} digits.'
    default_regex = '^\d{%d}$'

    def __init__(self, digits_number, **kwargs):
        regex = kwargs.pop('regex', self.default_regex % digits_number)
        error = kwargs.pop('error', self.default_message.format(num=digits_number))
        super().__init__(regex, error=error, **kwargs)


class Login(Regexp):
    _login_chars = 'A-Za-z0-9._-'
    default_message = 'Value must contains only {chars} characters.'.format(chars=_login_chars)
    default_regex = '^[%s]*$' % _login_chars

    def __init__(self, **kwargs):
        regex = kwargs.pop('regex', self.default_regex)
        error = kwargs.pop('error', self.default_message)
        super().__init__(regex, error=error, **kwargs)
