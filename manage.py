#!venv/bin/python
import os
import unittest
import coverage
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'api/__init__.py',
        'api/tests/*',
        'api/*/__init__.py'
    ]
)
COV.start()

from api import app, db

__author__ = 'Kostel Serhii'

migrate = Migrate(app, db)
manager = Manager(app)


# db (migrations)
manager.add_command('db', MigrateCommand)


# runserver
# TODO: move port and debug into config
server = Server(host="0.0.0.0", port=7254, use_debugger=True)
manager.add_command('runserver', server)


# tests
def _api_test():
    tests_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'api/tests')
    suite = unittest.TestLoader().discover(tests_path, pattern='*.py')
    return unittest.TextTestRunner(verbosity=2).run(suite)


@manager.command
def test():
    """Runs unit tests into api/tests path."""
    result = _api_test()
    return 0 if result.wasSuccessful() else 1


@manager.command
def test_cover():
    """Runs the unit tests into api/tests path with coverage."""
    result = _api_test()
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'test_cover')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
