import os

from datetime import datetime


class Base:

    BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(BASE_FOLDER, 'frontend', 'static')

    # Define the database
    SQLALCHEMY_DATABASE_URI = 'postgresql://xopclient:G5MuJkzyAXQhslCQ@localhost/xopclientdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False      # flask-sql signaling not used now

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "rx$iyDi~~ztvGj$q|pUVQSmBD07gSWTPswP{H3vKQ0HkvSKnzj"

    SECRET_KEY = "twuDcr%V#QQ8i*J8DW3k9XNG{~|266~0I?5ek1Zy4HMF4w{KPwfsddf4456"

    # Current versions:
    API_VERSION = 'dev'
    BUILD_DATE = datetime(2016, 3, 22, 18, 55, 42, 768858)

    PUBLIC_KEY_FILE_NAME = BASE_FOLDER + '/public.pem'


class Production(Base):
    pass


class Debug(Base):
    DEBUG = True

    # Current links:
    PROCESSING_URL = 'http://192.168.1.122:8888'  # TODO: Write down the right Processing-server address.
    ADMIN_API_URL = "http://localhost:7128/api/admin/dev"

    NOTIFICATION_SERVER_URL = 'amqp://remote:remote@192.168.1.113:5672//'  # TODO: Write down the right Admin-server address.

    # Queue:
    QUEUE_HOST_ADDRESS = 'amqp://guest:guest@192.168.1.118:5672//'  # TODO: Write down the right queue-server address (without port).
    QUEUE_NAME = 'hello'  # TODO: Write down the right queue name.


class Testing(Debug):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = "postgresql://xopclienttest:test123@localhost/xopclienttestdb"
    PUBLIC_KEY_FILE_NAME = Base.BASE_FOLDER + '/test_public.pem'
