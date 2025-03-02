from df_user import user_decorator
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse
from django.db.models import Sum

from .models import *


@user_decorator.login
def user_cart(request):
    uid = request.session["user_id"]
    carts = CartInfo.objects.filter(user_id=uid)
    count = CartInfo.objects.filter(user_id=request.session["user_id"]).aggregate(
        Sum("count")
    )["count__sum"]
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # How many items the current user purchased
        return JsonResponse({"count": count, "cart_num": count})
    else:
        context = {
            "title": "Shopping Cart",
            "page_name": 1,
            "carts": carts,
            "cart_num": count,
        }
        return render(request, "df_cart/cart.html", context)


@user_decorator.login
def add(request, gid, count):
    uid = request.session["user_id"]
    gid, count = int(gid), int(count)
    print(f"uid: {uid}, gid: {gid}, count: {count},")
    # Check if there is already this product in the shopping cart, if so, increase the quantity, if not, add it
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    count = CartInfo.objects.filter(user_id=uid).aggregate(Sum("count"))["count__sum"]
    print(f"count in add: {count}")
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"count": count})
    else:
        context = {
            "cart_num": count,
        }
        return render(request, "df_cart/cart.html", context)


@user_decorator.login
def edit(request, cart_id, count):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data["count"] = 0
    except Exception:
        data["count"] = count
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data["ok"] = 1
    except Exception:
        data["ok"] = 0
    return JsonResponse(data)
