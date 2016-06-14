import os
import decimal
import logging
import logging.handlers
from datetime import datetime
from functools import wraps
from flask import Flask, Blueprint, json, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.contrib.fixers import ProxyFix

__author__ = 'Kostel Serhii'


db = SQLAlchemy()
migrate = Migrate()

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/client/dev')
pages = Blueprint('pages', __name__)


# App created notifier

_app_created_subscribers = set()


def _inform_app_created(app):
    """Send app to every subscribers."""
    for func in _app_created_subscribers:
        func(app)


def after_app_created(func):
    """Subscribe function to call after app created."""
    _app_created_subscribers.add(func)
    return wraps(func)


# Extended JSON encoder

class XOPayJSONEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)

        if isinstance(obj, datetime):
            # datetime in format: YYYY-MM-DDThh:mm:ss±hh:mm
            if not obj.tzinfo:
                raise TypeError(repr(obj) + ' timezone missing')
            return obj.strftime('%Y-%m-%dT%H:%M:%S%z')

        return super(XOPayJSONEncoder, self).default(obj)


def logger_configure(log_config):

    if 'LOG_FILE' in log_config and os.access(os.path.dirname(log_config['LOG_FILE']), os.W_OK):
        log_handler = logging.handlers.RotatingFileHandler(
            filename=log_config['LOG_FILE'],
            maxBytes=log_config['LOG_MAX_BYTES'],
            backupCount=log_config['LOG_BACKUP_COUNT'],
            encoding='utf8',
        )
    else:
        log_handler = logging.StreamHandler()

    log_formatter = logging.Formatter(fmt=log_config['LOG_FORMAT'], datefmt=log_config['LOG_DATE_FORMAT'])
    log_handler.setFormatter(log_formatter)

    # root logger
    logging.getLogger('').addHandler(log_handler)
    logging.getLogger('').setLevel(log_config['LOG_ROOT_LEVEL'])

    # local logger
    logging.getLogger(log_config.get('LOG_BASE_NAME', '')).setLevel(log_config['LOG_LEVEL'])


app = Flask(__name__)
app.config.from_object('config.Production')
app.static_folder = app.config["STATIC_FOLDER"]

app.wsgi_app = ProxyFix(app.wsgi_app)
app.json_encoder = XOPayJSONEncoder

logger_configure(app.config)
log = logging.getLogger('xop.main')
log.info('Starting XOPay Client Service...')

# in production werkzeug logger does not work
# add requests log manually
if not app.config['DEBUG']:

    @app.after_request
    def log_request(response):
        request_detail = dict(
            remote_address=request.remote_addr,
            method=request.method,
            path=request.full_path if request.query_string else request.path,
            status=response.status_code
        )
        logging.getLogger('xop.request').info('[%(remote_address)s] %(method)s %(path)s %(status)s' % request_detail)
        return response

db.app = app
db.init_app(app)
migrate.init_app(app, db)

import api.handlers
from api import views

app.register_blueprint(api_v1)
app.register_blueprint(pages)

_inform_app_created(app)

