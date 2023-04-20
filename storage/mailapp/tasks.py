from celery import shared_task
from django.core.mail import send_mail
from storage import settings


@shared_task(bind=True)
def send_notification_mail(self, subject, recipients, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False,
        )
    return "Done"
