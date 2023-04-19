from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def rent_boxes(request):
    return render(request, 'boxes.html')


def show_faq(request):
    return render(request, 'faq.html')


def show_user_rent(request):
    return render(request, 'my-rent.html')


def show_user_rent_empty(request):
    return render(request, 'my-rent-empty.html')