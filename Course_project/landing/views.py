from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *

import datetime

def landing(request):
    name = "Maksimka"
    current_date = datetime.date.today()
    form = SubscriberForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print(request.POST)
        print(form.cleaned_data)
        data = form.cleaned_data
        print(data["name"])

        new_form = form.save()
    return render(request, 'landing/landing.html',locals())
# Create your views here.

def home(requsest):
    products_images = ProductImage.objects.filter(is_active=True,is_main=True, product__is_active=True)
    products_images_laptops = products_images.filter(product__category_id=1)
    products_images_phones = products_images.filter(product__category_id=2)
    products_images_tablets = products_images.filter(product__category_id=3)
    return render(requsest, 'landing/home.html',locals())

def about(request):
    return  render(request,'about.html',locals())
