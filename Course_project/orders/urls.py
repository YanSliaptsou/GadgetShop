from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^landing/',views.landing,name = 'landing')
    url(r'^add_to_basket/',views.add_to_basket,name = 'add_to_basket'),
    url(r'^checkout/$', views.checkout,name='checkout'),
    url(r'^admin_orders',views.admin_orders,name='admin_orders'),
]