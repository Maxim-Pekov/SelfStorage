import uuid
import qrcode

from django.conf import settings
from django.shortcuts import render
from mailapp.tasks import send_notification_mail
from stock_app.models import Storage


def index(request):
    if request.method == 'POST' and 'EMAIL' in request.POST:
        process_welcome_email(request)

    return render(request, 'index.html')


def rent_boxes(request):
    boxes = Storage.objects.all()
    context = {
        'boxes': boxes
    }
    return render(request, 'boxes.html', context=context)


def show_faq(request):
    return render(request, 'faq.html')


def show_user_rent(request):
    if request.method == 'POST' and 'box_id' in request.POST:
        process_open_box(request)
    return render(request, 'my-rent.html')


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


def process_open_box(request):

    user_mail = 'aslepaugo@gmail.com'

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
