from itertools import chain
from marshmallow import Schema as _Schema, fields, ValidationError, validates_schema
from marshmallow.validate import Regexp

__author__ = 'Kostel Serhii'


def deep_diff(new, previous):
    """
    Return dict object, that is different between object and origin.
    Do NOT get diff of the list objects! Just return them.
    :param new: initial dict for deference
    :param previous: original dict, that will be subtracted from initial
    :return: difference dict between initial and origin
    """
    if not previous:
        return new

    flat = lambda obj: not isinstance(obj[1], (dict, list))
    initial_flat_pairs, origin_flat_pairs = set(filter(flat, new.items())), set(filter(flat, previous.items()))
    initial_dict_pairs = filter(lambda obj: isinstance(obj[1], dict), new.items())
    initial_list_pairs = filter(lambda obj: isinstance(obj[1], list), new.items())

    recurse_dict_pairs = ((key, deep_diff(value, previous.get(key, {}))) for key, value in initial_dict_pairs)

    diff = dict(chain(initial_flat_pairs - origin_flat_pairs,
                      filter(lambda obj: bool(obj[1]), recurse_dict_pairs),
                      initial_list_pairs))
    return diff


class BaseSchema(_Schema):

    def __init__(self, *args, **kwargs):
        partial_nested = kwargs.pop('partial_nested', False)
        if partial_nested:
            self._make_partial_nested()

        super().__init__(*args, **kwargs)

    def _make_partial_nested(self):
        for field_name, field in self._declared_fields.items():
            if isinstance(field, fields.Nested):
                setattr(field.nested, 'partial', True)

    @validates_schema
    def validate_not_blank(self, data):
        if data is None or not str(data):
            raise ValidationError('Wrong request body or Content-Type header missing')

    def load(self, data, origin_model=None, **kwargs):
        """
        Serialize and validate data json.
        :param data: dict to deserialize
        :param origin_model: model instance of the origin object. If specified, load only changed values.
        :return: UnmarshalResult
        """
        if origin_model:
            # get serialized origin dict from model
            origin = self.dump(origin_model).data
            data = deep_diff(data, origin)

        return super().load(data, **kwargs)


# Validators


class Phone(Regexp):

    default_message = 'Wrong phone format.'
    default_regex = '^[1-9]{1}[0-9]{3,14}$'

    def __init__(self, **kwargs):
        regex = kwargs.pop('regex', self.default_regex)
        super().__init__(regex, **kwargs)
