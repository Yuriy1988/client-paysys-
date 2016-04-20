from celery import Celery

from api import app, errors


def send_email(email, subject, message):
    try:
        Celery(broker=app.config["NOTIFICATION_SERVER_URL"]).send_task('notify.send_mail', (email, subject, message))
    except Exception as ex:
        raise errors.ServiceUnavailable("Notification service is unavailable now.")
    return "Message sent to {email}".format(email=email)


def notify(email, payment):
    return send_email(
        email,
        "XOPAY transaction status",
        "Thank you for your payment! Transaction status is: {status}".format(status=payment.status)
    )
