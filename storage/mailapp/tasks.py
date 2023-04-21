from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from email.mime.image import MIMEImage
from storage import settings
from stock_app.models import Order


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
            with open(f"{settings.MEDIA_ROOT}/{image_name}", mode='rb') as f:
                image = MIMEImage(f.read())
                image.add_header('Content-ID', f"<{image_name}>")
                message.attach(image)

    message.send()
    return "Done"


@shared_task(bind=True)
def check_rent_remainder(self):
    rent_reminder_days = settings.START_RENT_REMINDER_DAYS
    orders = Order.objects.filter(
        paid_till__lte=timezone.now() + timezone.timedelta(days=rent_reminder_days),
        paid_till__gte=timezone.now()
    )
    print(f"Orders to be notified: {len(orders)}")
    for order in orders:
        days_left = (order.paid_till - timezone.now()).days + 1
        rent_end_date = order.paid_till.strftime('%d.%m.%Y')
        print(f"{days_left=}, {rent_end_date=} {order.box.title=}, {order.box.storage.title=}, {order.client.email=}")
        send_notification_mail.delay(
            subject=f'Reminder about rent end. Box {order.box.title}. Storage {order.box.storage.title}',
            recipients=[order.client.email],
            template='rent_reminder.html',
            context={
                'days_left': days_left,
                'rent_end_date': rent_end_date,
            }
        )
    print('Rent has been checked')

    return "Done"
