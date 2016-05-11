import os


class _Base:
    LOG_CONFIG = "log_config.json"

    # Paths
    BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(BASE_FOLDER, 'frontend', 'static')
    PUBLIC_KEY_FILE_NAME = BASE_FOLDER + '/public.pem'

    # Date base
    SQLALCHEMY_DATABASE_URI = 'postgresql://xopclient:G5MuJkzyAXQhslCQ@127.0.0.1/xopclientdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Current versions:
    API_VERSION = 'dev'
    BUILD_DATE = '2016-04-16T17:09:00+00:00'

    # Security
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "rx$iyDi~~ztvGj$q|pUVQSmBD07gSWTPswP{H3vKQ0HkvSKnzj"

    SECRET_KEY = "twuDcr%V#QQ8i*J8DW3k9XNG{~|266~0I?5ek1Zy4HMF4w{KPwfsddf4456"


class Debug(_Base):
    DEBUG = True

    SERVER_NAME = '127.0.0.1:7254'

    # Current links:
    PROCESSING_URL = '127.0.0.1:8888'  # TODO: Write down the right Processing-server address.
    ADMIN_API_URL = "http://127.0.0.1:7128/api/admin/dev"

    # Queue:
    QUEUE_HOST = '0.0.0.0'
    QUEUE_PORT = 5672
    QUEUE_USERNAME = 'xopay_rabbit'
    QUEUE_PASSWORD = '5lf01xiOFwyMLvQrkzz7'
    QUEUE_VIRTUAL_HOST = '/xopay'

    QUEUE_TRANS_FOR_PROCESSING='transactions_for_processing'
    QUEUE_EMAIL = 'notify_email'
    QUEUE_SMS = 'notify_sms'


class Production(_Base):
    DEBUG = False

    SERVER_NAME = 'xopay.digitaloutlooks.com'

    # Current links:
    PROCESSING_URL = '127.0.0.1:8888'  # TODO: Write down the right Processing-server address.
    ADMIN_API_URL = "http://127.0.0.1:7128/api/admin/dev"

    # Queue:
    QUEUE_HOST = '0.0.0.0'
    QUEUE_PORT = 5672
    QUEUE_USERNAME = 'xopay_rabbit'
    QUEUE_PASSWORD = '5lf01xiOFwyMLvQrkzz7'
    QUEUE_VIRTUAL_HOST = '/xopay'

    QUEUE_TRANS_FOR_PROCESSING='transactions_for_processing'
    QUEUE_EMAIL='notify_email'
    QUEUE_SMS='notify_sms'


class Testing(_Base):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Date base
    SQLALCHEMY_DATABASE_URI = "postgresql://xopclienttest:test123@127.0.0.1/xopclienttestdb"

    # Paths
    PUBLIC_KEY_FILE_NAME = _Base.BASE_FOLDER + '/test_public.pem'
