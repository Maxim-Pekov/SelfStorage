from django.shortcuts import render
from stock_app.models import Storage, Box
from mailapp.tasks import send_notification_mail
from django.shortcuts import redirect
import uuid
from yookassa import Configuration, Payment
from django.conf import settings


def index(request):
    if request.method == 'POST' and 'EMAIL' in request.POST:
        process_welcome_email(request)

    return render(request, 'index.html')


def rent_boxes(request):
    storages = Storage.objects.all()
    boxes = Box.objects.all()
    context = {
        'storages': storages,
        'boxes': boxes
    }
    return render(request, 'boxes.html', context=context)


def payment_view(request, boxnumber):
    boxes = boxnumber

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_API_KEY

    payment = Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com/"
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())
    context = {
        'boxes': boxes
    }
    return redirect(payment.confirmation.confirmation_url)


def show_faq(request):
    return render(request, 'faq.html')


def show_user_rent(request):
    return render(request, 'my-rent.html')


def show_user_rent_empty(request):
    return render(request, 'my-rent-empty.html')


def process_welcome_email(request):
    user_mail = request.POST.get('EMAIL')
    if user_mail:
        send_notification_mail.delay(
            subject='Welcome to our storage',
            recipients=[user_mail],
            template='welcome.html',
            context={
                'user_mail': user_mail,
                'inline_images': ['img1.png'],
            }
        )
