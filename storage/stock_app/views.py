from django.shortcuts import render
from stock_app.models import Storage
from mailapp.tasks import send_notification_mail


def index(request):
    print(request.method)
    if request.method == 'POST':
        user_mail = request.POST.get('EMAIL')
        print(user_mail)
        if user_mail:
            send_notification_mail.delay(
                subject='Welcome to our storage',
                recipients=[user_mail],
                message='Thank you for your attention to our storage service. We will reach you soon.'
            )

        return render(request, 'index.html')

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