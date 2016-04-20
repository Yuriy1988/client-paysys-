#!venv/bin/python
import os
import unittest
import flask_script as script
import flask_migrate as migrate

from api import app, db

__author__ = 'Kostel Serhii'

manager = script.Manager(app)

# runserver
server = script.Server(host="0.0.0.0", port=7254, use_debugger=True)
manager.add_command('runserver', server)


# test
def test():
    base = os.path.dirname(os.path.realpath(__file__))

    api_tests_path = os.path.join(base, 'api', 'tests')
    api_suite = unittest.TestLoader().discover(api_tests_path, pattern='*.py')

    unittest.TextTestRunner(verbosity=2).run(api_suite)

test_command = script.Command(test)
manager.add_command('test', test_command)


# db migrations
migration = migrate.Migrate(app, db)
manager.add_command('db', migrate.MigrateCommand)


if __name__ == "__main__":
    manager.run()
