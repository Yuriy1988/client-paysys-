import decimal
import logging
from logging import FileHandler, Formatter

from flask import Flask, json
from flask.ext.cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# allow cross-origin ajax
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# DB and Migrations:
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Logging:
# FIXME: write correct log configuration and add logs
# file_handler = FileHandler('./error.log')
# file_handler.setLevel(logging.WARNING)
# file_handler.setFormatter(Formatter(
#     '''
#     NEW_LOG:
#     Time:        %(asctime)s
#     Level Name:  %(levelname)s:
#     Message:     %(message)s
#     Pass:        [in %(pathname)s:%(lineno)d]
#     '''
# ))
# app.logger.addHandler(file_handler)


# Decimal-to-json fix:
class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder

from api import handlers
