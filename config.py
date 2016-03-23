import os

from datetime import datetime

DEBUG = True

BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
FRONTEND_FOLDER = os.path.join(BASE_FOLDER, 'frontend')
STATIC_FOLDER = os.path.join(FRONTEND_FOLDER, 'static')

# Define the database
SQLALCHEMY_DATABASE_URI = 'postgresql://xopclientadmin:xopclient@localhost/xopclientdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False      # flask-sql signaling not used now

CSRF_ENABLED = True
CSRF_SESSION_KEY = "mhe=d4#2xvb1348j%m+sn0d8ssdbjv18yi+f_w#&yd!+&4ic4)"

SECRET_KEY = "ugGB0uH1cJTW=1L9Vs|8roMlFfFgsWD%NA|*WBpYQ3Uytr-6rImVk2Rp%BJ+"

# Current links:
HELPER_URL = 'http://192.168.1.122:8888'  # TODO: Write down the right Helper-server address.
PROCESSING_URL = 'http://192.168.1.122:8888'  # TODO: Write down the right Processing-server address.
ADMIN_URL = 'http://127.0.0.1:7128' # TODO: Write down the right Admin-server address.

# Queue:
QUEUE_HOST_ADDRESS = 'localhost'  # TODO: Write down the right queue-server address (without port).
QUEUE_NAME = 'hello'  # TODO: Write down the right queue name.

# Current versions:
API_VERSION = 'dev'
CURRENT_CLIENT_SERVER_VERSION = 'dev'
CURRENT_ADMIN_SERVER_VERSION = 'dev'
BUILD_DATE = datetime(2016, 3, 22, 18, 55, 42, 768858)
