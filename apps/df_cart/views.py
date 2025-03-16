from df_user import user_decorator
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse
from django.db.models import Sum

from .models import *

def user_cart(request):
    uid = request.session.get("user_id")

    if uid:  # Nếu user đã đăng nhập -> lấy từ DB
        carts = CartInfo.objects.filter(user_id=uid)
        count = carts.aggregate(Sum("count"))["count__sum"] or 0
    else:  # Nếu là khách -> lấy từ session
        guest_cart = request.session.get("guest_cart", {})
        count = sum(guest_cart.values())
        carts = []

    print("count:", count)
    context = {
        "title": "Shopping Cart",
        "page_name": 1,
        "carts": carts,
        "cart_num": count,
    }
    return render(request, "df_cart/cart.html", context)


def add(request, gid, count):
    gid, count = gid, int(count)
    uid = request.session.get("user_id")

    if uid:  # Nếu user đã đăng nhập, lưu vào DB
        cart, created = CartInfo.objects.get_or_create(
            user_id=uid,
            goods_id=gid,
            defaults={"count": count},
        )
        if not created:
            cart.count += count
            cart.save()

        cart_count = CartInfo.objects.filter(user_id=uid).aggregate(Sum("count"))["count__sum"]
    
    else:  # Nếu là khách, lưu vào session
        guest_cart = request.session.get("guest_cart", {})
        guest_cart[gid] = guest_cart.get(gid, 0) + count
        request.session["guest_cart"] = guest_cart
        request.session.modified = True  # Bắt buộc Django lưu session ngay lập tức
        cart_count = sum(guest_cart.values())

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"count": cart_count})
    
    context = {"cart_num": cart_count}
    return render(request, "df_cart/cart.html", context)

# @user_decorator.login
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


# @user_decorator.login
def delete(request, cart_id):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data["ok"] = 1
    except Exception:
        data["ok"] = 0
    return JsonResponse(data)
