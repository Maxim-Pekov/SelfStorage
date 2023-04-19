from django.shortcuts import render
from stock_app.models import Storage


def index(request):
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