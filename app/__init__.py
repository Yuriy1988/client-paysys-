from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import logging
from logging import FileHandler, Formatter


app = Flask(__name__)
app.config.from_object('config')

# DB and Migrations:
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Logging:
file_handler = FileHandler('./error.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(Formatter(
    '''
    NEW_LOG:
    Time:        %(asctime)s
    Level Name:  %(levelname)s:
    Message:     %(message)s
    Pass:        [in %(pathname)s:%(lineno)d]
    '''
))
app.logger.addHandler(file_handler)


from app import handlers


