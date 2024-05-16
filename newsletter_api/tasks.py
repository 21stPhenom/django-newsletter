from django.core.mail import send_mail
from celery import shared_task

from config.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_email_task(email_address, message):
    send_mail(
        'Test Mail',
        f'This is the message you typed: {message}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email_address]
    )