import os
import decimal
import logging
import logging.handlers
from datetime import datetime
from functools import wraps
from flask import Flask, Blueprint, json
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


# Create application

app = Flask(__name__)
app.config.from_object('config.Debug')
app.static_folder = app.config["STATIC_FOLDER"]

app.wsgi_app = ProxyFix(app.wsgi_app)
app.json_encoder = XOPayJSONEncoder

db.app = app
db.init_app(app)
migrate.init_app(app, db)

import api.handlers
from api import views

app.register_blueprint(api_v1)
app.register_blueprint(pages)

import api.logger

_inform_app_created(app)

log = logging.getLogger('xop.main')
log.info('Starting XOPay Client Service...')