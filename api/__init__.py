import decimal

from flask import Flask, json
from flask.ext.cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import STATIC_FOLDER


app = Flask(__name__, static_folder=STATIC_FOLDER)
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


# Decimal-to-json fix:
class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app.json_encoder = MyJSONEncoder

from api import handlers
