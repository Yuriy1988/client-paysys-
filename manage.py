#!venv/bin/python

import flask_script as script
import flask_migrate as migrate
from client import app, db
from client.models import *


migration = migrate.Migrate(app, db)
manager = script.Manager(app)
manager.add_command('db', migrate.MigrateCommand)


@manager.command
def create_db():
    return db.create_all()


if __name__ == "__main__":
    manager.run()
