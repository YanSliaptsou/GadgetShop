from django.contrib import admin
from .models import *

class ProductInOrderInline(admin.TabularInline):
    model = ProdutInOrder
    extra = 0

class StatusAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Status._meta.fields]
    
    class Meta:
        model = Status


admin.site.register(Status,StatusAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)

class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProdutInOrder._meta.fields]

    class Meta:
        model = ProdutInOrder


admin.site.register(ProdutInOrder, ProductInOrderAdmin)

class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProdutInBasket._meta.fields]

    class Meta:
        model = ProdutInBasket


admin.site.register(ProdutInBasket, ProductInBasketAdmin)

#Register your models here.
