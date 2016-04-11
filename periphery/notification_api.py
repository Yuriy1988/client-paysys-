from celery import Celery

from config import NOTIFICATION_SERVER_URL


def send_email(email, subject, message):
    Celery(broker=NOTIFICATION_SERVER_URL).send_task('notify.send_mail', (email, subject, message))
    return "Message sent to {email}".format(email=email)
