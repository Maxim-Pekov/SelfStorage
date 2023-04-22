import uuid
import qrcode

from django.shortcuts import render
from stock_app.models import Storage, Box, Client
from mailapp.tasks import send_notification_mail
from django.shortcuts import redirect
from yookassa import Configuration, Payment
from django.conf import settings


def index(request):
    if request.method == 'POST' and 'EMAIL' in request.POST:
        process_welcome_email(request)

    return render(request, 'index.html')


def storage_view(request, storage):
    storages = Storage.objects.all()
    boxes = Box.objects.calculate_box_square().filter(storage__id=storage)
    boxes_lower_3_square = boxes.filter(box_square__lt=3).filter(storage__id=storage)
    boxes_lower_10_square = boxes.filter(box_square__lt=10).filter(storage__id=storage)
    boxes_upper_10_square = boxes.filter(box_square__gte=10).filter(storage__id=storage)
    context = {
        'storages': storages,
        'boxes': boxes,
        'boxes_lower_3_square': boxes_lower_3_square,
        'boxes_lower_10_square': boxes_lower_10_square,
        'boxes_upper_10_square': boxes_upper_10_square,
        'x': 'abc'
    }
    return render(request, 'boxes.html', context=context)


def payment_view(request, boxnumber):
    boxes = Box.objects.get(id=boxnumber)

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_API_KEY

    payment = Payment.create({
        "amount": {
            "value": boxes.price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://80.249.146.130/my-rent/1"
        },
        "capture": True,
        "description": f"Бокс №{boxes.title} - "
                       f"Цена {boxes.price} - "
                       f"Длина {boxes.length} - "
                       f"Ширина {boxes.width} - "
                       f"Высота {boxes.height}"
    }, uuid.uuid4())
    return redirect(payment.confirmation.confirmation_url)


def show_faq(request):
    return render(request, 'faq.html')


def show_user_rent(request, user_id):
    client = Client.objects.get(id=user_id)
    context = {
        'client': client
    }
    if request.method == 'POST' and 'box_id' in request.POST:
        process_open_box(request, client)
    return render(request, 'my-rent.html', context)


def show_user_rent_empty(request):
    return render(request, 'my-rent-empty.html')


def process_welcome_email(request):
    user_mail = request.POST.get('EMAIL')
    if not user_mail:
        return "Error"
    send_notification_mail.delay(
        subject='Welcome to our storage',
        recipients=[user_mail],
        template='welcome.html',
        context={
            'user_mail': user_mail,
            'inline_images': ['img1.png'],
        }
    )
    return "Done"


def process_open_box(request, client):

    user_mail = client.email

    box_id = request.POST.get('box_id')
    if not box_id:
        return "Error"
    qr_code_uuid = uuid.uuid4()
    qr_data = {
        'box_id': box_id,
        'user_id': 1,
        'uuid': qr_code_uuid,
        'timestamp': '2021-01-01 00:00:00',
    }
    qr_image = qrcode.make(qr_data)
    qr_image_name = f'qr_code_{qr_code_uuid}.png'
    qr_image.save(f'{settings.MEDIA_ROOT}/{qr_image_name}')
    send_notification_mail.delay(
        subject='Your box is ready',
        recipients=[user_mail],
        template='open_box.html',
        context={
            'box_id': box_id,
            'qr_code_uuid': qr_code_uuid,
            'inline_images': ['img1.png', qr_image_name],
        }
    )
    return "Done"
