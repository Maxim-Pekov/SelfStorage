from django.shortcuts import render
from stock_app.models import Storage
from mailapp.tasks import send_notification_mail


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
