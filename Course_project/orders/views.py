from django.db.models import Count
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from utils.emails import SendingEmail

def add_to_basket(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProdutInBasket.objects.filter(id=product_id).update(is_active = False)
    else:
        new_product, created = ProdutInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})

        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProdutInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)

def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProdutInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)


    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            email = data["email"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, customer_email=email, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProdutInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProdutInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=order)
            #email = SendingEmail()
            #email.sending_email(type_id=1,order=order)
            #email.sending_email(type_id=2,email=order.customer_email,order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

def merging_dicts(l1,l2,key1,key2):
        merged = {}
        for item in l1:
            merged[item[key1]] = item
        for item in l2:
            try:
                if "products" in merged[item[key2]]:
                    merged[item[key2]]["products"].append(item)
                else:
                    merged[item[key2]]["products"] = [item]

            except Exception as e:
                return True

        orders = [val for (_,val) in merged.items()]

        return orders

def admin_orders(request):

    user = request.user
    if user.is_superuser:
        orders = Order.objects.all().annotate(products_nmb = Count('produtinorder')).values()
        orders_ids = [order["id"] for order in orders]

        products_in_order = ProdutInOrder.objects.filter(is_active=True,order_id__in=orders_ids)\
        .values("order_id", "product__name", "nmb", "price_per_item", "total_price")


        orders = merging_dicts(list(orders),list(products_in_order),"id","order_id")

        return render(request,'orders/admin_orders.html',locals())
    else:
        return HttpResponseRedirect(reversed("home"))


