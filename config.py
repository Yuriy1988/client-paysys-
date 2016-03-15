import os


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

HELPER_URL = 'http://192.168.1.122:8888'  # TODO: Write down the rigth Helper-server adress.
PROCESSING_URL = 'http://192.168.1.122:8888'  # TODO: Write down the rigth Processing-server adress.

CURRENT_API_VERSION = 'dev'
