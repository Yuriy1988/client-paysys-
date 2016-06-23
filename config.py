import os
from datetime import timedelta

__author__ = 'Kostel Serhii'


class _Base:

    # Paths
    BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(BASE_FOLDER, 'frontend', 'static')
    PUBLIC_KEY_FILE_NAME = BASE_FOLDER + '/public.pem'

    SERVICE_NAME = 'xopay-client'

    AFTER_REQUEST_TRACK_ENABLE = False
    AFTER_REQUEST_LOGGER_ENABLE = False

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

    LOG_BASE_NAME = 'xop'
    LOG_FORMAT = '%(levelname)-6.6s | CLIENT | %(name)-12.12s | %(asctime)s | %(message)s'
    LOG_DATE_FORMAT = '%d.%m %H:%M:%S'
    LOG_REQUESTS = False

    AUTH_ALGORITHM = 'HS512'
    AUTH_KEY = 'PzYs2qLh}2$8uUJbBnWB800iYKe5xdYqItRNo7@38yW@tPDVAX}EV5V31*ZK78QS'
    AUTH_TOKEN_LIFE_TIME = timedelta(minutes=30)
    AUTH_SYSTEM_USER_ID = 'xopay.client'

    ACCESS_TOKEN_LIFE_TIME = timedelta(days=1)


class Debug(_Base):
    DEBUG = True

    # FIXME: uncomment after config update (for full invite url)
    # SERVER_NAME = '127.0.0.1:7254'

    LOG_ROOT_LEVEL = 'INFO'
    LOG_LEVEL = 'DEBUG'

    # Current links:
    ADMIN_API_URL = "http://127.0.0.1:7128/api/admin/dev"

    # Queue:
    QUEUE_HOST = '0.0.0.0'
    QUEUE_PORT = 5672
    QUEUE_USERNAME = 'xopay_rabbit'
    QUEUE_PASSWORD = '5lf01xiOFwyMLvQrkzz7'
    QUEUE_VIRTUAL_HOST = '/xopay'

    QUEUE_TRANS_FOR_PROCESSING = 'transactions_for_processing'
    QUEUE_3D_SECURE_RESULT = '3d_secure_result'
    QUEUE_EMAIL = 'notify_email'
    QUEUE_SMS = 'notify_sms'
    QUEUE_REQUEST = 'notify_request'


class Production(_Base):
    DEBUG = False

    # FIXME: uncomment after config update (for full invite url)
    # SERVER_NAME = 'xopay.digitaloutlooks.com'

    AFTER_REQUEST_TRACK_ENABLE = True
    AFTER_REQUEST_LOGGER_ENABLE = True

    LOG_ROOT_LEVEL = 'INFO'
    LOG_LEVEL = 'INFO'

    LOG_FILE = '/var/log/xopay/xopay.log'
    LOG_MAX_BYTES = 10*1024*1024
    LOG_BACKUP_COUNT = 10

    # Current links:
    ADMIN_API_URL = "http://127.0.0.1:7128/api/admin/dev"

    # Queue:
    QUEUE_HOST = '0.0.0.0'
    QUEUE_PORT = 5672
    QUEUE_USERNAME = 'xopay_rabbit'
    QUEUE_PASSWORD = '5lf01xiOFwyMLvQrkzz7'
    QUEUE_VIRTUAL_HOST = '/xopay'

    QUEUE_TRANS_FOR_PROCESSING = 'transactions_for_processing'
    QUEUE_3D_SECURE_RESULT = '3d_secure_result'
    QUEUE_EMAIL = 'notify_email'
    QUEUE_SMS = 'notify_sms'
    QUEUE_REQUEST = 'notify_request'


class Testing(_Base):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    LOG_ROOT_LEVEL = 'INFO'
    LOG_LEVEL = 'INFO'

    # Date base
    SQLALCHEMY_DATABASE_URI = "postgresql://xopclienttest:test123@127.0.0.1/xopclienttestdb"

    # Paths
    PUBLIC_KEY_FILE_NAME = _Base.BASE_FOLDER + '/test_public.pem'
