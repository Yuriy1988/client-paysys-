from api import errors


def handle_service_unavailable_error(msg):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as ex:
                print(ex)
                raise errors.ServiceUnavailable(msg)
            return result
        return wrapped
    return decorator
