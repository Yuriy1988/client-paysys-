import os
from datetime import timedelta

__author__ = 'Kostel Serhii'


class debug:

    SERVICE_NAME = 'xopay-client'
    BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
    PUBLIC_KEY_FILE_NAME = os.path.join(BASE_FOLDER, 'public.pem')

    # Common
    ADMIN_PORT = 7128
    CLIENT_PORT = 7254

    ADMIN_API_VERSION = 'dev'
    CLIENT_API_VERSION = 'dev'

    @property
    def ADMIN_API_URL(self):
        return 'http://127.0.0.1:%s/api/admin/%s' % (self.ADMIN_PORT, self.ADMIN_API_VERSION)

    @property
    def CLIENT_API_URL(self):
        return 'http://127.0.0.1:%s/api/client/%s' % (self.CLIENT_PORT, self.CLIENT_API_VERSION)

    # Local
    HOST = '127.0.0.1'
    PORT = CLIENT_PORT
    PREFERRED_URL_SCHEME = 'http'

    DEBUG = True
    AFTER_REQUEST_TRACK_ENABLE = False
    AFTER_REQUEST_LOGGER_ENABLE = False

    SERVER_NAME = '%s:%d' % (HOST, PORT)

    # Logger
    LOGGER_NAME = 'xop'
    LOG_FORMAT = '%(levelname)-6.6s | CLIENT | %(name)-12.12s | %(asctime)s | %(message)s'
    LOG_DATE_FORMAT = '%d.%m %H:%M:%S'

    LOG_ROOT_LEVEL = 'INFO'
    LOG_LEVEL = 'DEBUG'

    # Auth
    AUTH_ALGORITHM = 'HS512'
    # TODO: generate AUTH_KEY for production and copy to every service
    AUTH_KEY = 'PzYs2qLh}2$8uUJbBnWB800iYKe5xdYqItRNo7@38yW@tPDVAX}EV5V31*ZK78QS'
    AUTH_TOKEN_LIFE_TIME = timedelta(minutes=30)
    AUTH_SYSTEM_USER_ID = SERVICE_NAME

    ACCESS_TOKEN_LIFE_TIME = timedelta(days=1)

    # Database
    DB_NAME = 'xopclientdb'
    DB_USER = 'xopclient'
    DB_PASSWORD = 'G5MuJkzyAXQhslCQ'

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return 'postgresql://%s:%s@localhost/%s' % (self.DB_USER, self.DB_PASSWORD, self.DB_NAME)

    # Queue:
    QUEUE_HOST = '0.0.0.0'
    QUEUE_PORT = 5672
    QUEUE_USERNAME = 'xopay_rabbit'
    QUEUE_VIRTUAL_HOST = '/xopay'
    QUEUE_PASSWORD = '5lf01xiOFwyMLvQrkzz7'

    QUEUE_TRANS_FOR_PROCESSING = 'transactions_for_processing'
    QUEUE_3D_SECURE_RESULT = '3d_secure_result'
    QUEUE_EMAIL = 'notify_email'
    QUEUE_SMS = 'notify_sms'
    QUEUE_REQUEST = 'notify_request'

    # Flask
    STATIC_FOLDER = os.path.join(BASE_FOLDER, 'frontend/static')
    SECRET_KEY = "twuDcr%V#QQ8i*J8DW3k9XNG{~|266~0I?5ek1Zy4HMF4w{KPwfsddf4456"
    CSRF_SESSION_KEY = "rx$iyDi~~ztvGj$q|pUVQSmBD07gSWTPswP{H3vKQ0HkvSKnzj"
    CSRF_ENABLED = True


class test(debug):

    TESTING = True
    DEBUG = True
    AFTER_REQUEST_TRACK_ENABLE = False
    AFTER_REQUEST_LOGGER_ENABLE = False

    PRESERVE_CONTEXT_ON_EXCEPTION = False

    LOG_ROOT_LEVEL = 'WARNING'
    LOG_LEVEL = 'WARNING'

    AUTH_TOKEN_LIFE_TIME = timedelta(minutes=10)

    DB_NAME = 'xopclienttestdb'
    DB_USER = 'xopclienttest'
    DB_PASSWORD = 'test123'

    @property
    def PUBLIC_KEY_FILE_NAME(self):
        return os.path.join(self.BASE_FOLDER, 'test_public.pem')


class production(debug):

    PREFERRED_URL_SCHEME = 'https'

    DEBUG = False
    AFTER_REQUEST_TRACK_ENABLE = True
    AFTER_REQUEST_LOGGER_ENABLE = True

    SERVER_NAME = 'xopay.digitaloutlooks.com'

    LOG_ROOT_LEVEL = 'INFO'
    LOG_LEVEL = 'INFO'

    LOG_FILE = '/var/log/xopay/xopay.log'
    LOG_MAX_BYTES = 10*1024*1024
    LOG_BACKUP_COUNT = 10


class ConfigLoader(dict):
    """ Load config with config_name."""

    def __init__(self, config_name='debug'):
        super().__init__()

        xop_config_obj = globals()[config_name]
        if not xop_config_obj:
            return

        config_instance = xop_config_obj()
        for key in dir(config_instance):
            if key.isupper():
                self[key] = getattr(config_instance, key)
