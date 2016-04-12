from celery import Celery

from api import app


def send_email(email, subject, message):
    Celery(broker=app.config["NOTIFICATION_SERVER_URL"]).send_task('notify.send_mail', (email, subject, message))
    return "Message sent to {email}".format(email=email)
