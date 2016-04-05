import sys
from traceback import format_exception
from flask import jsonify

from api import app

__author__ = 'Kostel Serhii'


def _error_serializer(message, status_code, errors=None, traceback=None):
    """
    Error serializer in format:
    {
        error: {
            status_code: status_code,
            message: message,
            errors: {               // optional
                ...
            },
            traceback: traceback    // optional
    }
    :param status_code: error http code
    :param message: error message
    :param errors: dict with additional information about errors
    :param traceback: fall detail (in debug mode)
    :return: json error
    """
    error_dict = {'message': message, 'status_code': status_code}
    if errors:
        error_dict['errors'] = errors
    if traceback:
        error_dict['traceback'] = traceback

    response = jsonify(error=error_dict)
    response.status_code = status_code
    return response


def _handle_api_error(cls):
    """
    Decorator to handle API errors
    :param cls: BaseAPIError class instance
    """
    @app.errorhandler(cls)
    def _handler(err):
        return _error_serializer(message=err.message, status_code=err.status_code, errors=err.errors)
    return cls


def _handle_default_error(error, status_code, message=None, with_traceback=False):
    """
    Handler for default error
    :param error: Exception class instance
    :param status_code: error http code
    :return: serialized error
    """
    message = message or getattr(error, 'description', str(error))
    traceback = None
    if with_traceback and app.config['DEBUG']:
        etype, value, tb = sys.exc_info()
        traceback = ''.join(format_exception(etype, value, tb))
    return _error_serializer(message=message, status_code=status_code, traceback=traceback)


# API Errors


@_handle_api_error
class BaseApiError(Exception):

    default_status_code = 400
    default_message = 'Bad Request'

    def __init__(self, message=None, status_code=None, errors=None):
        super().__init__(self)
        self.message = message or self.default_message
        self.status_code = status_code or self.default_status_code
        self.errors = errors


@_handle_api_error
class ValidationError(BaseApiError):

    default_status_code = 400
    default_message = 'Request with invalid arguments'


@_handle_api_error
class NotFoundError(BaseApiError):

    default_status_code = 404
    default_message = 'Not Found'


# Default Errors


@app.errorhandler(400)
def error_bad_request(error):
    return _handle_default_error(error, 400, with_traceback=True)


@app.errorhandler(404)
def error_not_found(error):
    return _handle_default_error(error, 404)


@app.errorhandler(405)
def error_method_not_allowed(error):
    return _handle_default_error(error, 405)


@app.errorhandler(500)
def error_internal_server_error(error):
    return _handle_default_error(error, 500, with_traceback=True)

