from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from storage import settings


@shared_task(bind=True)
def send_notification_mail(self, subject, recipients, template, context):
    html_content = render_to_string(template_name=template, context=context).strip()
    message = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipients,
        reply_to=[settings.EMAIL_REPLY_TO],
        )
    message.content_subtype = 'html'
    message.mixed_subtype = 'related'

    if context.get('inline_images'):
        for image_name in context.get('inline_images'):
            with open(f"media/{image_name}", mode='rb') as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', f"<{image_name}>")
                message.attach(image)

    message.send()
    return "Done"
