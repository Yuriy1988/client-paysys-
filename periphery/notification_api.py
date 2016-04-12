from celery import Celery

from api import app
from periphery.service_error import handle_service_unavailable_error


@handle_service_unavailable_error(msg="Notification service is unavailable now.")
def send_email(email, subject, message):
    Celery(broker=app.config["NOTIFICATION_SERVER_URL"]).send_task('notify.send_mail', (email, subject, message))
    return "Message sent to {email}".format(email=email)
