import os
import decimal
import logging
import logging.config
from datetime import datetime
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, Blueprint, json
from flask_sqlalchemy import SQLAlchemy


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


app = Flask(__name__)
app.config.from_object('config.Production')
app.static_folder = app.config["STATIC_FOLDER"]

app.wsgi_app = ProxyFix(app.wsgi_app)
app.json_encoder = XOPayJSONEncoder

db = SQLAlchemy(app)

# Logging:
with open(os.path.join(app.config['BASE_FOLDER'], app.config['LOG_CONFIG']), 'rt') as f:
    log_config = json.load(f)
logging.config.dictConfig(log_config)
logging.getLogger("production")

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/client/dev')

import api.handlers
from api import views

app.register_blueprint(api_v1)
